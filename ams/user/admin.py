from django.contrib import admin

# Register your models here.
from user.models import Roles, Departments, Users

admin.site. register(Roles)
admin.site. register(Departments)
admin.site. register(Users)