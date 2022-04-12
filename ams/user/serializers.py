from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import Role, Department, MyUser


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role_name', 'description']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'shift_start', 'shift_end']


class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    department_details = DepartmentSerializer(source='department', read_only=True)

    class Meta:
        model = MyUser
        fields = ['id', 'name', 'password', 'role', 'device_id', 'department',
                  'department_details']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UsersSerializer, self).create(validated_data)


class UserListSerializer(serializers.ModelSerializer):
    department_details = DepartmentSerializer(source='department', read_only=True)

    class Meta:
        model = MyUser
        fields = ['id', 'device_id', 'name', 'role', 'department_details']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['device_id'] = user.device_id
        return token

