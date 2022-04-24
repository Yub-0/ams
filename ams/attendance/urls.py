from django.urls import path
from attendance.views import ViewAllAttendance, ViewDailyAttendance, SyncAttendanceView, TodaysReport, AttendanceOfUserView

from attendance import views


all_attendance = ViewAllAttendance.as_view({
    'get': 'list'  # simply view all attendance
})
all_DAttendance = ViewDailyAttendance.as_view({
    'get': 'list'  # view daily attendance
})
sync_Attendance = SyncAttendanceView.as_view({
    'post': 'create'  # sync all attendance from device
})
show_DailyReport = TodaysReport.as_view({
    'get': 'list'  # show days report
})
user_attendance = AttendanceOfUserView.as_view({
    'get': 'list'
})
urlpatterns = [
    path('viewAllAttendance', all_attendance, name='view all attendance(admin)'),
    path('viewDayAttendance', all_DAttendance, name='view todays attendance log(admin)'),
    path('syncAttendance/', sync_Attendance, name='sync all Attendance from device(admin)'),
    path('showReport', show_DailyReport, name='show todays report'),
    # path('attendanceDetail/', views.ViewAttendanceDetail.as_view(), name='view attendance details(user-specific)'),
    path('attendanceDetail/<int:pk>/', views.ViewAttendanceDetail.as_view(), name='view attendance details(user-specific)'),
    path('attendanceOfUser', user_attendance, )
]