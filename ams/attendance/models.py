from django.utils import timezone

from django.db import models

# Create your models here.
from django.db import models

# from user.models import Users
from user.models import MyUser


class DailyLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    arrival_time = models.TimeField(auto_now=False, blank=False, null=False)
    departure_time = models.TimeField(auto_now=False, blank=False, null=False)
    day = models.DateTimeField(default=timezone.now)
    remarks = models.TextField(default="")

    def __str__(self):
        return str(self.user.name)


class AttendanceLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id = models.BigIntegerField(null=False)
    timestamp = models.DateTimeField(null=False)
    c_type = models.IntegerField(null=False)

    def __str__(self):
        return str(self.timestamp)


