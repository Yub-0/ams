"""ams URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('attendance.urls')),
    path('', include('user.urls'))
]

# from django.urls import path
# from django.contrib import admin
# from user.views import Login, Dashboard, RolesView, UsersView, DepartmentsView,Logout,SyncUserView
# from company_calendar.views import HolidayView
# from attendance_logs.views import UserListView, UserReportView,AttendaceLogView,DailyReportView,UpdateAttendanceView
# from leave.views import LeaveView,UserLeaveView
# urlpatterns = [
#     path('dashboard/', Dashboard.as_view()),
#     path('login/', Login.as_view()),
#     path('logout/', Logout.as_view()),
#     path('', Login.as_view()),
#     path('users/roles/', RolesView.as_view()),
#     path('users/', UsersView.as_view()),
#     path('users/departments/', DepartmentsView.as_view()),
#     path('users/sync/', SyncUserView.as_view()),
#     path('users/leave/', LeaveView.as_view()),
#     path('users/leave/<int:device_id>/', LeaveView.as_view()),
#     path('users/leaveview/', UserLeaveView.as_view()),
#     path('users/leaveview/<int:device_id>/', UserLeaveView.as_view()),
#     path('calendar/holidays/', HolidayView.as_view()),
#     path('attendance/sync/', AttendaceLogView.as_view()),
#     path('attendance/users/', UserListView.as_view()),
#     path('attendance/update/', UpdateAttendanceView.as_view()),
#     path('attendance/users/<int:user_id>/', UserReportView.as_view()),
#     path('attendance/daily/report/', DailyReportView.as_view()),
#     path('admin/', admin.site.urls),
# ]