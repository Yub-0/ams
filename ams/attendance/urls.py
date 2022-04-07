from django.urls import path
from attendance.views import ViewAttendanceLog, ViewDailyAttendance, AttendanceSyncView, DaysReport

all_attendance = ViewAttendanceLog.as_view({ #simply view all attendance
    'get': 'list'
})
all_DAttendance = ViewDailyAttendance.as_view({ #view daily attendance
    'get': 'list'
})
sync_Attendance = AttendanceSyncView.as_view({ #sync all attendance from device
    'post': 'create'
})
show_DailyReport = DaysReport.as_view({ #show days report
    'get': 'list'
})
urlpatterns = [
    path('viewAllAttendance', all_attendance, name='all_attendance'),
    path('viewDayAttendance', all_DAttendance, name='all_dailyattendance'),
    path('syncAttendance/', sync_Attendance, name='syncAttendance'),
    path('showReport', show_DailyReport, name='daily_report'),
]