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
from .serializers import AttendanceLogSerializer, DailyLogsSerializer

IN_HOURS = 10
IN_MINUTES = 00
IN_THRESHOLD_MINUTES = 1
OUT_HOURS = 17
OUT_MINUTES = 00


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


# class DailyLogsView(mixins.CreateModelMixin,
#                     viewsets.GenericViewSet):
#         at = AttendanceLog.objects.all()
#         u = Users.objects.all()
#         for ats in at:
#             for us in u:
#                 if pd.to_datetime(ats.a_datetime).date() == datetime.date.today():
#                     if ats.device_id == us.device_id:
#                         if not DailyLogs.objects.filter(user=ats.device_id,
#                                                         ).exists():
#                             DailyLogs.objects.create(
#                                 user=ats.device_id,
#                                 arrival_time=pd.to_datetime(ats.a_datetime).time(),
#                                 leave_time=None,
#                                 day=ats.a_datetime.strftime("%A"),
#                                 remarks='Add Manually',
#                             )


class ViewAllAttendance(mixins.ListModelMixin,
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
    # print(at)

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
                    pagination_class = PageNumberPagination
                    queryset = DailyLogs.objects.all()
                    serializer_class = DailyLogsSerializer

                    def list(self, request):
                        # Note the use of `get_queryset()` instead of `self.queryset`
                        queryset = self.get_queryset()
                        serializer = DailyLogsSerializer(queryset, many=True)
                        return Response(serializer.data)
    for ats in at:
        if DailyLogs.objects.filter(user=ats.device_id,
                                    ).exists():
            print("here")
            print(pd.to_datetime(ats.timestamp).time())
            DailyLogs.objects.filter(user=ats.device_id).update(
                departure_time=pd.to_datetime(ats.timestamp).time(),
                remarks='helo Departed',
            )


#