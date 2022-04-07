from rest_framework import mixins, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from user.models import MyUser
from .models import DailyLog, AttendanceLog
import pandas as pd
import datetime
from .serializers import AttendanceLogSerializer, DailyLogsSerializer, DailyReportSerializer, AttendanceReportSerializer


class AttendanceSyncView(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):

    # def create(self, request):
        # conn = connect_device()
        # if conn is not None:
        #     attds = conn.get_attendance()
        #     # d_users = conn.get_users()
        #     conn.disconnect()
        #     for att in attds:
        #         if not AttendanceLog.objects.filter(device_id=att.user_id,
        #                                             timestamp=att.timestamp,
        #                                             c_type=att.status).exists():
        #             AttendanceLog.objects.create(
        #                 device_id=att.user_id,
        #                 timestamp=att.timestamp,
        #                 c_type=att.status
        #             )
        permission_classes = [IsAuthenticated, IsAdminUser, ]
        queryset = AttendanceLog.objects.all()
        serializer_class = AttendanceLogSerializer

        def create(self, request):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViewAttendanceLog(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    pagination_class = PageNumberPagination
    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceLogSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AttendanceLogSerializer(queryset, many=True)
        return Response(serializer.data)


class ViewDailyAttendance(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    at = AttendanceLog.objects.all()
    u = MyUser.objects.all()
    for ats in at:
        for us in u:
            # if pd.to_datetime(ats.timestamp).date() == datetime.date.today():
                if ats.device_id == us.device_id:
                    if not DailyLog.objects.filter(user=ats.device_id,
                                                   ).exists():
                        DailyLog.objects.create(
                            user=us,
                            arrival_time=pd.to_datetime(ats.timestamp).time(),
                            departure_time=pd.to_datetime(ats.timestamp).time(),
                            day=ats.timestamp.strftime("%A"),
                            remarks='Arrived',
                        )
    for ats in at:
        for us in u:
            if pd.to_datetime(ats.timestamp).date() == datetime.date.today():
                if ats.device_id == us.device_id:
                    if DailyLog.objects.filter(user=ats.device_id,
                                               ).exists():
                        DailyLog.objects.filter(user=ats.device_id).update(
                            departure_time=pd.to_datetime(ats.timestamp).time(),
                            remarks='Departed',
                        )

    pagination_class = PageNumberPagination
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogsSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = DailyLogsSerializer(queryset, many=True)
        return Response(serializer.data)


class DaysReport(mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    li = []
    u = MyUser.objects.all()
    d = DailyLog.objects.all()
    for de in d:
        for us in u:

            if not DailyLog.objects.filter(user=us).exists():
                report = [
                    {"device_id": us.device_id, "name": us.name, "status": 'Absent', "remarks": 'Not Arrived Yet'}]
                li.append(report)
            if us.device_id == de.user.device_id:
                if de.arrival_time > us.department.shift_start:
                    report = [{"device_id": us.device_id, "name": us.name, "status": 'Present', "remarks": 'Late'}]
                elif de.arrival_time < us.department.shift_start:
                    report = [{"device_id": us.device_id,  "name": us.name, "status": 'Present', "remarks": 'Early'}]
                else:
                    report = [{"device_id": us.device_id,  "name": us.name, "status": 'Present', "remarks": 'On_time'}
                    ]

                li.append(report)
                # queryset = li
    # for us in u:

    queryset = li

    def list(self, request):
        res = []
        queryset = self.get_queryset()
        for a in queryset:
            results = DailyReportSerializer(a, many=True).data
            res.append(results)

        return Response(res)



