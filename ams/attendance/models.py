from django.db import models
import datetime
from user.models import MyUser


class DailyLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    arrival_time = models.TimeField(auto_now=False, blank=False, null=False)
    departure_time = models.TimeField(auto_now=False, blank=True, null=True)
    day = models.DateField(default=datetime.date.today)
    remarks = models.TextField(default="")

    def __str__(self):
        return str(self.user.name)


class AttendanceLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id = models.BigIntegerField(null=False)
    time = models.TimeField(auto_now=False, blank=False, null=False)
    date = models.DateField(default=datetime.date.today)
    c_type = models.IntegerField(null=False)

    def __str__(self):
        return str(self.time)


