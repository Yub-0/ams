from django.urls import path
from attendance.views import ViewAttendanceLog, ViewDailyAttendance, AttendanceSyncView, DaysReport

from attendance import views

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
    path('viewAllAttendance', all_attendance, name='view all attendance(admin)'),
    path('viewDayAttendance', all_DAttendance, name='view todays attendance log(admin)'),
    path('syncAttendance/', sync_Attendance, name='sync all Attendance from device(admin)'),
    path('showReport', show_DailyReport, name='show todays report'),
    path('attendanceDetail/', views.ViewAttendanceDetail.as_view(), name='view attendance details(user-specific)'),
]