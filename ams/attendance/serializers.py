from rest_framework import serializers

from attendance.models import DailyLogs, AttendanceLog
from user.serializers import UsersSerializer


class DailyLogsSerializer(serializers.ModelSerializer):
    user_details = UsersSerializer(source='user', read_only=True)

    class Meta:
        model = DailyLogs
        fields = ['id', 'user', 'user_details', 'arrival_time', 'departure_time', 'day', 'remarks']


class AttendanceLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendanceLog
        fields = ['id', 'device_id', 'timestamp', 'c_type',]
