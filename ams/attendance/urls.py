from attendance import views
from django.urls import path

urlpatterns = [
    path('syncAttendance/', views.SyncAttendanceView.as_view(), name='sync all Attendance from device(admin)'),
    path('viewAllAttendance', views.ViewAllAttendance.as_view(), name='view all attendance(admin)'),
    path('viewAllAttendancePag', views.ViewAllAttendancePag.as_view(),
         name='view all attendance with pagiination(admin)'),
    path('attendanceOfUser', views.AttendanceOfUserView.as_view(), name='display attendance of logged in user only'),
    # path('viewDailyAttendance', views.ViewDailyAttendance.as_view(), name='view todays attendance log(admin)'),
    path('attendanceDetail/', views.ViewAttendanceDetail.as_view(), name='view attendance details'),
    path('attendanceDetail/<int:pk>/', views.ViewSpecificAttendance.as_view(),
         name='view attendance details(user-specific)'),
    path('report', views.ReportView.as_view()),
    path('showReport', views.TodaysReport.as_view(), name='show todays report'),
]