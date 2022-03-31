from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager


# Create your models here.
class Roles(models.Model):
    role = models.TextField(primary_key=True, max_length=100)
    description = models.TextField(null=True, blank=True)


class Departments(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    shift_start = models.TimeField(auto_now=False, blank=False, null=False)
    shift_end = models.TimeField(auto_now=False, blank=False, null=False)


class Users(AbstractBaseUser):
    REQUIRED_FIELDS = ['name', 'password', 'role']
    USERNAME_FIELD = 'id'

    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=False, blank=False)
    password = models.CharField(null=False, max_length=256)
    role = models.ForeignKey(Roles, on_delete=models.PROTECT)
    device_id = models.BigIntegerField(unique=True, null=False, blank=False)
    department = models.ForeignKey(Departments, on_delete=models.PROTECT)
    is_active = models.BooleanField(null=False, blank=False)

    objects = UserManager()

