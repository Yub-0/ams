from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ObjectDoesNotExist
from user.models import MyUser, Department, Role
from user.serializers import UserSerializer, RoleSerializer, DepartmentSerializer,\
    MyTokenObtainPairSerializer, UserListSerializer

from user.permissions import IsOwner, IsAdminUser


class RegisterUserView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class RegisterRolesView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    serializer_class = RoleSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class RegisterDepartmentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    serializer_class = DepartmentSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class RoleView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    queryset = Role.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = RoleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleDetail(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = RoleSerializer
    # lookup_field = 'pk'

    def get(self, request, pk):
        # id = request.GET.get('id')
        # instance = self.get_object()
        instance = Role.objects.get(id=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = Role.objects.get(id=pk)
        # instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "failed", "details": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        instance = Role.objects.get(id=pk)
        # instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    queryset = Department.objects.all()

    def get(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = DepartmentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepartmentDetail(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = DepartmentSerializer
    # lookup_field = 'pk'

    def get(self, request, pk):
        # instance = self.get_object()
        instance = Department.objects.get(id=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # instance = self.get_object()
        instance = Department.objects.get(id=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "failed", "details": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        # instance = self.get_object()
        instance = Department.objects.get(id=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            instance.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    queryset = MyUser.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = MyUser.objects.all()
    serializer_class = UserListSerializer
    lookup_field = 'pk'

    def get(self, request, pk):
        # user = self.get_object()
        try:
            user = MyUser.objects.get(device_id=pk)
        except ObjectDoesNotExist:
            return Response({"message": "No Such User"}, status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # instance = self.get_object()
        user = MyUser.objects.get(device_id=pk)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "failed", "details": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        # user = self.get_object()
        user = MyUser.objects.get(device_id=pk)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


