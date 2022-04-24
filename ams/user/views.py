import datetime

from rest_framework import mixins, viewsets, status, permissions, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import MyUser, Department, Role
from user.serializers import UserSerializer, RoleSerializer, DepartmentSerializer, MyTokenObtainPairSerializer, UserListSerializer

from user.permissions import IsOwner, IsAdminUser
from rest_framework import filters


class RegisterUserView(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif not serializer.data['name'] or not serializer.data['device_id'] or not serializer.data['role'] \
                or not serializer.data['department']:
            return Response({"message: Field cannot be empty!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif not serializer.data['password']:
            return Response({"message: Password cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"message": "User with device id already exists."}, status=status.HTTP_409_CONFLICT)
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class RegisterRolesView(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    serializer_class = RoleSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif not serializer.data['name']:
            print("hello", serializer.data['name'])
            return Response({"message": "Name cannot be Empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"message": "Role name already exists."}, status=status.HTTP_409_CONFLICT)


class RegisterDepartmentView(mixins.CreateModelMixin,
                             viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    serializer_class = DepartmentSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif not serializer.data['name'] or not serializer.data['shift_start'] or not serializer.data['shift_end']:
            print("hello", serializer.data['name'], serializer.data['shift_start'], serializer.data['shift_end'])
            return Response({"message": "Field cannot be Empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif not type(serializer.data['shift_start']) is datetime.time or not type(serializer.data['shift_end'] is datetime.time):
            return Response({"message": "Enter valid time"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"message": "Department name already exists."}, status=status.HTTP_409_CONFLICT)


class RolesView(mixins.ListModelMixin,
                viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    pagination_class = PageNumberPagination
    queryset = Role.objects.all()

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = RoleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'pk'

    # def get_queryset(self):
    #     return MyUser.objects.filter(device_id=self.kwargs['pk'])

    def retrieve(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "failed", "details": serializer.errors})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            instance.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentsView(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    pagination_class = PageNumberPagination
    queryset = Department.objects.all()

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = DepartmentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]

    # def get_queryset(self):
    #     return MyUser.objects.filter(device_id=self.kwargs['pk'])

    def retrieve(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "failed", "details": serializer.errors})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            instance.delete()
            return Response({"message": "Deleted"})
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListView(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser ]
    pagination_class = PageNumberPagination
    queryset = MyUser.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'role']

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserListSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]

    # def get_queryset(self):
    #     return MyUser.objects.filter(device_id=self.kwargs['pk'])

    def retrieve(self, request, pk):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "failed", "details": serializer.errors})

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            user.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer



