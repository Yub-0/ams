from django.urls import path
from attendance import views

urlpatterns = [
    path('viewAllAttendance', views.ViewAllAttendance.as_view(), name='view all attendance(admin)'),
    path('viewDayAttendance', views.ViewDailyAttendance.as_view(), name='view todays attendance log(admin)'),
    path('syncAttendance/', views.SyncAttendanceView.as_view(), name='sync all Attendance from device(admin)'),
    path('showReport', views.TodaysReport.as_view(), name='show todays report'),
    # path('attendanceDetail/', views.ViewAttendanceDetail.as_view(), name='view attendance details(user-specific)'),
    path('attendanceDetail/<int:pk>/', views.ViewAttendanceDetail.as_view(), name='view attendance details(user-specific)'),
    path('attendanceOfUser', views.AttendanceOfUserView.as_view(), )
]