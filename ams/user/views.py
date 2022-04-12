from rest_framework import mixins, viewsets, status, permissions, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import MyUser, Department, Role
from user.serializers import UsersSerializer, RolesSerializer, DepartmentSerializer, MyTokenObtainPairSerializer, UserListSerializer

from user.permissions import IsOwner, IsAdminUser


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
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    queryset = Role.objects.all()
    serializer_class = RolesSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisterDepartmentView(mixins.CreateModelMixin,
                             viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RolesView(mixins.ListModelMixin,
                viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
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
    permission_classes = [IsAuthenticated, IsAdminUser, ]
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
    permission_classes = [IsAuthenticated, IsAdminUser ]
    pagination_class = PageNumberPagination
    queryset = MyUser.objects.all()
    serializer_class = UserListSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UsersSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return MyUser.objects.filter(id=self.kwargs['pk'])


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

