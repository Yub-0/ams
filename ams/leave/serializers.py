from rest_framework import serializers

from leave.models import StaffLeave


class StaffLeaveSerializer(serializers.Serializer):

    class Meta:
        model = StaffLeave
        fields = ['id', 'date', 'description', 'user']