from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
from nepali_date import NepaliDate
import json
# from .utils import connect_device, disconnect_device
from rest_framework import mixins, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from user.models import Users
from compant_calendar.models import Holidays
# from leave.models import StaffLeave
from .models import DailyLogs, AttendanceLog
from django.http import HttpResponseRedirect
import pytz
import datetime as dt
# from .forms import AttendaceUpdateForm
import pandas as pd
# Create your views here.
from user.serializers import UsersSerializer
import datetime
from .serializers import AttendanceLogSerializer, DailyLogsSerializer, DailyReportSerializer, AttendanceReportSerializer
from user.models import Departments


class UserListView(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data)


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

        queryset = AttendanceLog.objects.all()
        serializer_class = AttendanceLogSerializer

        def create(self, request):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViewAttendanceLog(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
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
    at = AttendanceLog.objects.all()
    u = Users.objects.all()

    for ats in at:
        for us in u:
            if pd.to_datetime(ats.timestamp).date() == datetime.date.today():
                if ats.device_id == us.device_id:
                    if not DailyLogs.objects.filter(user=ats.device_id,
                                                    ).exists():
                        DailyLogs.objects.create(
                            user=us,
                            arrival_time=pd.to_datetime(ats.timestamp).time(),
                            departure_time=pd.to_datetime(ats.timestamp).time(),
                            day=ats.timestamp.strftime("%A"),
                            remarks='Arrived',
                        )
    for ats in at:
        if DailyLogs.objects.filter(user=ats.device_id,
                                    ).exists():
            DailyLogs.objects.filter(user=ats.device_id).update(
                departure_time=pd.to_datetime(ats.timestamp).time(),
                remarks='Departed',
            )

    pagination_class = PageNumberPagination
    queryset = DailyLogs.objects.all()
    serializer_class = DailyLogsSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = DailyLogsSerializer(queryset, many=True)
        return Response(serializer.data)


class DaysReport(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

        li = []
        u = Users.objects.all()
        d = DailyLogs.objects.all()
        for de in d:
            for us in u:
                if us.device_id == de.user.device_id:
                    if de.arrival_time > us.department.shift_start:
                        report = [{"device_id": us.device_id, "name": us.name, "status": 'Present', "remarks": 'Late'}]

                    elif de.arrival_time < us.department.shift_start:
                        report = [{"device_id": us.device_id,  "name": us.name, "status": 'Present', "remarks": 'Early'}]

                    else:
                        report = [{"device_id": us.device_id,  "name": us.name, "status": 'Present', "remarks": 'On_time'}]

                    li.append(report)
                    # queryset = li
        for us in u:
            if not DailyLogs.objects.filter(user=us).exists():
                report = [{"device_id": us.device_id,  "name": us.name, "status": 'Absent', "remarks": 'Not Arrived Yet'}]
                li.append(report)

        queryset = li

        def list(self, request):
            res = []
            queryset = self.get_queryset()
            for a in queryset:
                results = DailyReportSerializer(a, many=True).data
                res.append(results)

            return Response(res)


class AttendanceReport(mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceLogSerializer

    def list(self, request):
        queryset = self.get_queryset()
        result = AttendanceLogSerializer(queryset, many=True)
        return Response(result.data)

    # for us in u:
    #     if not DailyLogs.objects.filter(user=us).exists():
    #         print(us.name, 'is absent')



    # for de in d:
    #     if de.departure_time>Users.objects.filter(department=)
        # for de in d:
            # if not DailyReport.objects.filter(user=us).exists():
            #    if de.arrival_time>us.department.shift_start:
                    # DailyReport.objects.create(
                    #     user=us,
                    #     status=0,
                    #     remarks=0,
                    # )
    #             if de.arrival_time<us.department.shift_start:
    #                 DailyReport.objects.create(
    #                     user=us,
    #                     status=0,
    #                     remarks=1,
    #                 )
    #             if de.arrival_time==us.department.shift_start:
    #                 DailyReport.objects.create(
    #                     user=us,
    #                     status=0,
    #                     remarks=2,
    #                 )
    #
    # pagination_class = PageNumberPagination
    # queryset = DailyReport.objects.all()
    # serializer_class = DailyReportSerializer
    #
    # def list(self, request):
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = DailyReportSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #     #     # print(us.department.shift_start)
    #     #     if de.arrival_time>us.department.shift_start:
    #     #         print("late")
    #     #     else:
    #     #         print("early")