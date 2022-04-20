from rest_framework import mixins, viewsets, status, permissions, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import MyUser, Department, Role
from user.serializers import UsersSerializer, RolesSerializer, DepartmentSerializer, MyTokenObtainPairSerializer, UserListSerializer

from user.permissions import IsOwner, IsAdminUser
from rest_framework import filters


class RegisterUserView(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class RegisterRolesView(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated, IsAdminUser, ]
    queryset = Role.objects.all()
    serializer_class = RolesSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisterDepartmentView(mixins.CreateModelMixin,
                             viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated, IsAdminUser, ]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RolesView(mixins.ListModelMixin,
                viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated, IsAdminUser, ]
    pagination_class = PageNumberPagination
    queryset = Role.objects.all()
    serializer_class = RolesSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = RolesSerializer(queryset, many=True)
        return Response(serializer.data)


class DepartmentsView(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated, IsAdminUser, ]
    pagination_class = PageNumberPagination
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = DepartmentSerializer(queryset, many=True)
        return Response(serializer.data)


class UserListView(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated, IsAdminUser ]
    pagination_class = PageNumberPagination
    queryset = MyUser.objects.all()
    serializer_class = UserListSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'role']

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserListSerializer
    lookup_field = 'pk'
    # permission_classes = [IsOwner]

    # def get_queryset(self):
    #     return MyUser.objects.filter(device_id=self.kwargs['pk'])

    def retrieve(self, request, pk):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"})

        else:
            return Response({"message": "failed", "details": serializer.errors})

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            user.delete()
            return Response({"message": "Deleted"})
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer



