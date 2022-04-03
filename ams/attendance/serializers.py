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
        fields = ['id', 'device_id', 'timestamp', 'c_type', ]


class DailyReportSerializer(serializers.Serializer):

    device_id = serializers.IntegerField()
    name = serializers.CharField()
    status = serializers.CharField()
    remarks = serializers.CharField()

    class Meta:
        ordering = ['device_id']


class AttendanceReportSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    day = serializers.CharField()
    status = serializers.CharField()

