from rest_framework import mixins, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from user.models import Users, Departments, Roles
from user.serializers import UsersSerializer, RolesSerializer, DepartmentSerializer


class RegisterUserView(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisterRolesView(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisterDepartmentView(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RolesView(mixins.ListModelMixin,
                viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = RolesSerializer(queryset, many=True)
        return Response(serializer.data)


class DepartmentsView(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = DepartmentSerializer(queryset, many=True)
        return Response(serializer.data)