from attendance.views import UserListView
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from attendance.views import ViewAttendanceLog, ViewDailyAttendance, AttendanceSyncView, DaysReport, AttendanceReport

all_user = UserListView.as_view({
    'get': 'list',
})
all_attendance = ViewAttendanceLog.as_view({
    'get': 'list'
})

all_DAttendance = ViewDailyAttendance.as_view({
    'get': 'list'
})
ca = AttendanceSyncView.as_view({
    'post': 'create'
})
show_DailyReport = DaysReport.as_view({
    'get': 'list'
})
view_attendance_report = AttendanceReport.as_view({
    'get': 'list'
})
# sync_user = AttendanceLogView.as_view({
#     'post': 'create',
# })
urlpatterns = [
    path('users/', all_user, name='all_user'),
    # path('users/sync', sync_user, name='sync_user')
    path('viewAllAttendance', all_attendance, name='all_attendance'),
    path('viewDayAttendance', all_DAttendance, name='all_daysattendance'),
    path('syncAt', ca, name='syncAt'),
    path('showReport', show_DailyReport, name='daily_report'),
    path('AttendanceReport', view_attendance_report, name='attendancereport')
]