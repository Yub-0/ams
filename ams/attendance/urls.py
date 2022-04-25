from datetime import datetime
from attendance import views
from django.urls import path, register_converter


class DateConverter:
    regex = '\d{4}-\d{1,2}-\d{1,2}'
    format = '%Y-%m-%d'

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)


register_converter(DateConverter, 'date')

urlpatterns = [
    path('viewAllAttendance', views.ViewAllAttendance.as_view(), name='view all attendance(admin)'),
    path('viewDayAttendance', views.ViewDailyAttendance.as_view(), name='view todays attendance log(admin)'),
    path('syncAttendance/', views.SyncAttendanceView.as_view(), name='sync all Attendance from device(admin)'),
    path('showReport', views.TodaysReport.as_view(), name='show todays report'),
    # path('attendanceDetail/', views.ViewAttendanceDetail.as_view(), name='view attendance details(user-specific)'),
    path('attendanceDetail/<int:pk>/', views.test.as_view(), name='view attendance(user-specific)'),
    path('attendanceOfUser', views.AttendanceOfUserView.as_view(), name='display attendance of logged in user only'),
]