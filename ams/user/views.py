import jwt
from django.contrib.auth import authenticate
from django.http import HttpResponse
from pytz import unicode
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import MyUser, Department, Role
from user.serializers import UsersSerializer, RolesSerializer, DepartmentSerializer

# from user.authentication import ExampleAuthentication
from user.serializers import MyTokenObtainPairSerializer


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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
    permission_classes = [IsAuthenticated, IsAdminUser,]
    pagination_class = PageNumberPagination
    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data)

# class UserLogin(APIView):
#
#     def post(self, request, *args, **kwargs):
#         if not request.data:
#             return Response({'Error': "Please provide device_id/password"}, status="400")
#
#         device_id = request.data['device_id']
#         password = request.data['password']
#         try:
#             user = authenticate(device_id=device_id, password=password)
#         except MyUser.DoesNotExist:
#             return Response({'Error': "Invalid username/password"}, status="400")
#         if user:
#             payload = {
#                 'device_id': user.device_id,
#                 'role': user.role.id,
#             }
#             token = jwt.encode(payload, "SECRET_KEY")
#
#             return Response(
#                 {'token': token},
#                 status=200,
#                 content_type="application/json"
#             )
#         else:
#             return Response(
#                 json.dumps({'Error': "Invalid credentials"}),
#                 status=400,
#                 content_type="application/json"
#             )


class MyObtainTokenPairView(TokenObtainPairView):
    # permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

