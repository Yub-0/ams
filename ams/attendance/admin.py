from django.contrib import admin

# Register your models here.
from attendance.models import DailyLog, AttendanceLog

admin.site. register(DailyLog)
admin.site. register(AttendanceLog)