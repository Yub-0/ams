from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from user.models import Roles, Departments, Users


class RolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Roles
        fields = ['role', 'description']


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Departments
        fields = ['name', 'shift_start', 'shift_end']


class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    department_details = DepartmentSerializer(source='department', read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'name', 'password', 'role', 'device_id', 'department',
                  'department_details', 'is_active']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UsersSerializer, self).create(validated_data)