from django.db import models
from nepali_date import NepaliDate
from user.models import MyUser


class StaffLeave(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(null=False)
    description = models.TextField(null=False)
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)

    class Meta:
        unique_together = [['date', 'user']]

    def _get_bs_date(self):
        return NepaliDate.to_nepali_date(self.date)

    bs_date = property(_get_bs_date)

    def __str__(self):
        return str(self.user)