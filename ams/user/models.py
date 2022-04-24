from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext as _
from user.managers import CustomUserManager


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.role_name


class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    shift_start = models.TimeField(auto_now=False, blank=False, null=False)
    shift_end = models.TimeField(auto_now=False, blank=False, null=False)

    def __str__(self):
        return self.name


class MyUser(AbstractBaseUser, PermissionsMixin):
    device_id = models.BigIntegerField(_('device_id'), primary_key=True)
    name = models.CharField(null=False, blank=False, max_length=25)
    password = models.CharField(null=False, max_length=256)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['name', 'password', 'role', 'department']
    USERNAME_FIELD = 'device_id'

    objects = CustomUserManager()

    def __str__(self):
        return str(self.device_id)
