from rest_framework import mixins, viewsets, status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from user.models import MyUser
from .models import DailyLog, AttendanceLog
import pandas as pd
import datetime
from .serializers import AttendanceSerializer, DailyLogsSerializer, DailyReportSerializer, AttendanceReportSerializer
from user import permissions
from attendance.permissions import IsOwner
from leave.models import StaffLeave


class SyncAttendanceView(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):

# def create(self, request):
#     conn = connect_device()
#     if conn is not None:
#         attds = conn.get_attendance()
#         # d_users = conn.get_users()
#         conn.disconnect()
#         for att in attds:
#             if not AttendanceLog.objects.filter(device_id=att.user_id,
#                                                 timestamp=att.timestamp,
#                                                 c_type=att.status).exists():
#                 AttendanceLog.objects.create(
#                     device_id=att.user_id,
#                     time=pd.to_datetime(att.timestamp).date(),
#                     date=pd.to_datetime(att.timestamp).time(),
#                     c_type=att.status
#                 )
    permission_classes = [IsAuthenticated, IsAdminUser, ]
    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AttendanceOfUserView(mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        courses = AttendanceLog.objects.filter(device_id=user.device_id)
        serializer = AttendanceSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewAllAttendance(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated, IsAdminUser, ]
    pagination_class = PageNumberPagination
    queryset = AttendanceLog.objects.all()
    # serializer_class = AttendanceSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AttendanceSerializer(queryset, many=True)
        return Response(serializer.data)


class ViewAttendanceDetail(generics.RetrieveAPIView):
    serializer_class = DailyLogsSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        print(self.kwargs['pk'])
        return DailyLog.objects.filter(user=self.kwargs['pk'])


class ViewDailyAttendance(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated, IsAdminUser, ]
    at = AttendanceLog.objects.all()
    u = MyUser.objects.all()
    for ats in at:
        if ats.date == datetime.date.today():
            for us in u:
                if ats.device_id == us.device_id:
                    if not DailyLog.objects.filter(user=ats.device_id,
                                                   ).exists():
                        DailyLog.objects.create(
                            user=us,
                            arrival_time=ats.time,
                            departure_time=ats.time,
                            day=ats.date,
                            remarks='Arrived',
                        )
    for ats in at:
        if ats.date == datetime.date.today():
            for us in u:
                if ats.device_id == us.device_id:
                    if DailyLog.objects.filter(user=ats.device_id,
                                               ).exists():
                        DailyLog.objects.filter(user=ats.device_id).update(
                            departure_time=ats.time,
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


class TodaysReport(mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated, IsAdminUser, ]
    li = []
    u = MyUser.objects.all()
    d = DailyLog.objects.all()
    sl = StaffLeave.objects.all()
    for us in u:
        if not us.device_id == 1:
            if not DailyLog.objects.filter(user=us).exists():
                for leave in sl:
                    if leave.user == us:
                        report = [
                            {"device_id": us.device_id, "name": us.name, "status": 'On Leave',
                             "remarks": leave.description}]
                        li.append(report)
                if not StaffLeave.objects.filter(user=us).exists():
                    report = [
                        {"device_id": us.device_id, "name": us.name, "status": 'Absent',
                        "remarks": 'Not Arrived Yet'}]
                    li.append(report)

    for da in d:
        if not da.day == datetime.date.today():
            for leave in sl:
                if leave.user == da.user:
                    report = [
                        {"device_id": da.user.device_id, "name": da.user.name, "status": 'On Leave',
                         "remarks": leave.description}]
                    li.append(report)
            if not StaffLeave.objects.filter(user=da.user).exists():
                report = [
                    {"device_id": da.user.device_id, "name": da.user.name, "status": 'Absent',
                    "remarks": 'Not Arrived Yet'}]
                li.append(report)

    for de in d:
        # print(pd.to_datetime(de.day).date())
        # print(datetime.date.today())
        if de.day == datetime.date.today():
            de_id = de.user.device_id
            u_name = de.user.name

            if de.arrival_time > de.user.department.shift_start and de.departure_time <= de.user.department.shift_end:
                report = [{"device_id": de_id, "name": u_name, "status": 'Present',
                           "remarks": 'Arrived late departed early', }]
            elif de.arrival_time > de.user.department.shift_start and de.departure_time >= de.user.department.shift_end:
                report = [{"device_id": de_id, "name": u_name, "status": 'Present',
                           "remarks": 'Arrived late departed late', }]
            elif de.arrival_time < de.user.department.shift_start and de.departure_time <= de.user.department.shift_end:
                report = [{"device_id": de_id,  "name": u_name, "status": 'Present',
                           "remarks": 'Arrived early departed early'}]
            elif de.arrival_time < de.user.department.shift_start and de.departure_time >= de.user.department.shift_end:
                report = [{"device_id": de_id,  "name": u_name, "status": 'Present',
                           "remarks": 'Arrived early departed late'}]

            li.append(report)
        # else:
        #     for leave in sl:
        #         if leave.user == de.user:
        #             report = [
        #                 {"device_id": de.user.device_id, "name": de.user.name, "status": 'On Leave',
        #                  "remarks": leave.description}]
        #             li.append(report)
        #     if not StaffLeave.objects.filter(user=de.user).exists():
        #         report = [
        #             {"device_id": de.user.device_id, "name": de.user.name, "status": 'Absent',
        #             "remarks": 'Not Arrived Yet'}]
        #         li.append(report)

    queryset = li

    def list(self, request):
        res = []
        queryset = self.get_queryset()
        for a in queryset:
            results = DailyReportSerializer(a, many=True).data
            res.append(results)

        return Response(res)




