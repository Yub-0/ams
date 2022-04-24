from rest_framework import serializers

from leave.models import StaffLeave
from user.serializers import UserSerializer


class StaffLeaveSerializer(serializers.ModelSerializer):
    # user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = StaffLeave
        fields = ['id', 'date', 'description', 'user', ]
