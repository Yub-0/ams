from attendance.views import UserListView
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from attendance.views import ViewAllAttendance, ViewDailyAttendance, AttendanceSyncView


all_user = UserListView.as_view({
    'get': 'list',
})
all_attendance = ViewAllAttendance.as_view({
    'get': 'list'
})

all_DAttendance = ViewDailyAttendance.as_view({
    'get': 'list'
})
ca = AttendanceSyncView.as_view({
    'post': 'create'
})
# cd = DailyLogsView.as_view()

# sync_user = AttendanceLogView.as_view({
#     'post': 'create',
# })
urlpatterns = format_suffix_patterns([
    path('users/', all_user, name='all_user'),
    # path('users/sync', sync_user, name='sync_user')
    path('viewAllAttendance', all_attendance, name='all_attendance'),
    path('viewDailyAttendance', all_DAttendance, name='all_dailyattendance'),
    path('syncAt', ca, name='syncAt'),
    # path('syncDa', cd, name='synceDa')
])