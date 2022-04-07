from django.db import models

# Create your models here.
from django.db import models

# from user.models import Users
from user.models import MyUser

DAYS = [
    ('0', 'Sunday'),
    ('1', 'Monday'),
    ('2', 'Tuesday'),
    ('3', 'Wednesday'),
    ('4', 'Thursday'),
    ('5', 'Friday'),
    ('6', 'Saturday')
]


class DailyLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    arrival_time = models.TimeField(auto_now=False, blank=False, null=False)
    departure_time = models.TimeField(auto_now=False, blank=False, null=False)
    day = models.CharField(max_length=25, choices=DAYS, default=0)
    remarks = models.TextField(default="")


class AttendanceLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id = models.BigIntegerField(null=False)
    timestamp = models.DateTimeField(null=False)
    c_type = models.IntegerField(null=False)


