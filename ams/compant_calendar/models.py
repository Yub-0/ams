from django.db import models
from nepali_date import NepaliDate


class Holidays(models.Model):
    id = models.BigAutoField(primary_key=True)
    day = models.DateField(null=False)
    description = models.TextField(null=False)

    def _get_bs_date(self):
        return NepaliDate.to_nepali_date(self.day)

    bs_date = property(_get_bs_date)