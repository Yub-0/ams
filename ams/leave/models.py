from django.db import models

# Create your models here.
from django.db import models
from nepali_date import NepaliDate
# from user.models import Users
from user.models import MyUser


class StaffLeave(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(null=False)
    description = models.TextField(null=False)
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)


    def _get_bs_date(self):
        return NepaliDate.to_nepali_date(self.date)

    bs_date = property(_get_bs_date)