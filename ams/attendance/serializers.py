from rest_framework import serializers

from attendance.models import DailyLog, AttendanceLog

from user.serializers import UserListSerializer


class DailyLogsSerializer(serializers.ModelSerializer):
    user_details = UserListSerializer(source='user', read_only=True)

    class Meta:
        model = DailyLog
        fields = ['id', 'user_details', 'arrival_time', 'departure_time', 'day', 'remarks']


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendanceLog
        fields = ['id', 'device_id', 'time', 'date']


class DailyReportSerializer(serializers.Serializer):
    device_id = serializers.IntegerField()
    name = serializers.CharField()
    status = serializers.CharField()
    remarks = serializers.CharField()

