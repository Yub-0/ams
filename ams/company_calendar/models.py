
from django.db import models


class Holiday(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_date = models.DateField(null=False, unique=True)
    end_date = models.DateField(unique=True, null=True)
    description = models.TextField(null=False)


