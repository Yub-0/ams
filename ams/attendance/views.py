from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from user.models import MyUser
from .models import DailyLog, AttendanceLog
import datetime
from datetime import timedelta
from rest_framework.filters import OrderingFilter
from .pagination import CustomPagination
from .serializers import AttendanceSerializer, DailyLogsSerializer, DailyReportSerializer
from attendance.permissions import IsOwner
from leave.models import StaffLeave


class SyncAttendanceView(generics.CreateAPIView):

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
#     permission_classes = [IsAuthenticated, IsAdminUser, ]
    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViewAllAttendance(generics.ListAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser, ]
    queryset = AttendanceLog.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = AttendanceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewAllAttendancePag(generics.ListAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser, ]
    queryset = AttendanceLog.objects.all().order_by("date")

    def get(self, request):
        pagination_class = CustomPagination
        paginator = pagination_class()
        queryset = self.get_queryset()
        page = paginator.paginate_queryset(queryset, request)
        serializer = AttendanceSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class AttendanceOfUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        at = AttendanceLog.objects.filter(device_id=user.device_id)
        serializer = AttendanceSerializer(at, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DailyAttendanceOfUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        da = DailyLog.objects.filter(user=user.device_id)
        serializer = DailyLogsSerializer(da, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewAttendanceDetail(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pagination_class = CustomPagination
        paginator = pagination_class()
        user = self.request.user
        if user.role.name == "Admin":
            device_id = request.GET.get('device_id')
            start_date = request.GET.get('sdate')
            end_date = request.GET.get('edate')
            if start_date and end_date and device_id is not None:
                attds = AttendanceLog.objects.filter(device_id=device_id, date__range=[start_date, end_date])
            elif start_date and end_date is not None:
                attds = AttendanceLog.objects.filter(date__range=[start_date, end_date])
            elif device_id is not None:
                attds = AttendanceLog.objects.filter(device_id=device_id)

            page = paginator.paginate_queryset(attds, request)
            attds = AttendanceSerializer(page, many=True).data
            return paginator.get_paginated_response(attds)

            # return Response(attds)
        else:
            return Response({'message': "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class ViewSpecificAttendance(generics.GenericAPIView):

    def get(self, request, pk):
        user = self.request.user
        if user.device_id == pk or user.role.name == "Admin":
            time = request.GET.get('time')
            start_date = request.GET.get('sdate')
            end_date = request.GET.get('edate')
            if start_date and end_date is not None:
                attds = AttendanceLog.objects.filter(device_id=pk,date__range=[start_date, end_date])
            elif time is not None:
                attds = AttendanceLog.objects.filter(device_id=pk, time=time)
            else:
                attds = AttendanceLog.objects.filter(device_id=pk)
            attds = AttendanceSerializer(attds, many=True).data
            return Response(attds)
        else:
            return Response({'message': "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class ReportView(generics.GenericAPIView):
    queryset = DailyLog.objects.all()

    def get(self, request):
        at = AttendanceLog.objects.all()
        u = MyUser.objects.all()
        for ats in at:
            for us in u:
                if us.device_id == ats.device_id:
                    if not DailyLog.objects.filter(user=us, day=ats.date
                                                   ).exists():
                        DailyLog.objects.create(
                            user=us,
                            arrival_time=ats.time,
                            departure_time=None,
                            day=ats.date,
                            remarks='Arrived',
                        )
                    elif DailyLog.objects.filter(user=us, day=ats.date
                                                 ).exists():
                        DailyLog.objects.filter(user=us, day=ats.date).update(
                            departure_time=ats.time,
                            remarks='Departed',
                        )

        today = datetime.date.today()
        yesterday = today - timedelta(days=1)
        user = self.request.user
        if user.role.name == "Admin":
            start_date = request.GET.get('sdate')
            end_date = request.GET.get('edate')
            if start_date and end_date is not None:
                attds = DailyLog.objects.filter(day__range=[start_date, end_date])
            else:
                attds = DailyLog.objects.filter(day__range=[yesterday, yesterday])
            attds = DailyLogsSerializer(attds, many=True).data
            return Response(attds)
        else:
            return Response({'message': "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        # queryset = self.get_queryset()
        # serializer = DailyLogsSerializer(queryset, many=True)
        # return Response(serializer.data)


class ViewTodayReport(generics.GenericAPIView):
    today = datetime.date.today()
    queryset = DailyLog.objects.filter(day=today)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = DailyLogsSerializer(queryset, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)
# class ViewDailyAttendance(generics.ListAPIView):
#     permission_classes = [IsAuthenticated, IsAdminUser, ]
#     queryset = DailyLog.objects.all()
#
#     def get(self, request):
#         at = AttendanceLog.objects.all()
#         u = MyUser.objects.all()
#         d = DailyLog.objects.all()
#         for ats in at:
#             if ats.date == datetime.date.today():
#                 for us in u:
#                     if us.device_id == ats.device_id:
#                         if not DailyLog.objects.filter(user=us, day=datetime.date.today()
#                                                        ).exists():
#
#                             DailyLog.objects.create(
#                                 user=us,
#                                 arrival_time=ats.time,
#                                 departure_time=None,
#                                 day=ats.date,
#                                 remarks='Arrived',
#                             )
#                         # else:
#                         #     DailyLog.objects.filter(user=ats.device_id, departure_time=None,
#                         #                             day=datetime.date.today()).update(
#                         #         departure_time=ats.time,
#                         #         remarks='Departed',
#                         #     )
#                         else:
#                             for de in d:
#                                 if de.arrival_time and de.departure_time is None:
#                                     DailyLog.objects.filter(user=ats.device_id, departure_time=None,
#                                                             day=datetime.date.today()).update(
#                                         departure_time=ats.time,
#                                         remarks='Departed',
#                                     )
#                                 elif de.arrival_time and de.departure_time:
#                                     DailyLog.objects.create(
#                                         user=us,
#                                         arrival_time=ats.time,
#                                         departure_time=None,
#                                         day=ats.date,
#                                         remarks='Arrived again',
#                                     )
#                                 else:
#                                     DailyLog.objects.create(
#                                         user=us,
#                                         arrival_time=ats.time,
#
#                                         departure_time=None,
#                                         day=ats.date,
#                                         remarks='Arrived',
#                                     )
#
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = DailyLogsSerializer(queryset, many=True)
#         return Response(serializer.data)


class TodaysReport(generics.ListAPIView):
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

    # for de in d:
    #     # print(pd.to_datetime(de.day).date())
    #     # print(datetime.date.today())
    #     if de.day == datetime.date.today():
    #         de_id = de.user.device_id
    #         u_name = de.user.name
    #
    #         if de.arrival_time > de.user.department.shift_start and de.departure_time <= de.user.department.shift_end:
    #             report = [{"device_id": de_id, "name": u_name, "status": 'Present',
    #                        "remarks": 'Arrived late departed early', }]
    #         elif de.arrival_time > de.user.department.shift_start and de.departure_time >= de.user.department.shift_end:
    #             report = [{"device_id": de_id, "name": u_name, "status": 'Present',
    #                        "remarks": 'Arrived late departed late', }]
    #         elif de.arrival_time < de.user.department.shift TodaysReport,_start and de.departure_time <= de.user.department.shift_end:
    #             report = [{"device_id": de_id,  "name": u_name, "status": 'Present',
    #                        "remarks": 'Arrived early departed early'}]
    #         elif de.arrival_time < de.user.department.shift_start and de.departure_time >= de.user.department.shift_end:
    #             report = [{"device_id": de_id,  "name": u_name, "status": 'Present',
    #                        "remarks": 'Arrived early departed late'}]
    #
    #         li.append(report)
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

    def get(self, request):
        res = []
        queryset = self.get_queryset()
        for a in queryset:
            results = DailyReportSerializer(a, many=True).data
            res.append(results)

        return Response(res)




