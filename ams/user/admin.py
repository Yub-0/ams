from django.contrib import admin

# Register your models here.
from user.models import Department, Role, MyUser

admin.site. register(Role)
admin.site. register(Department)
admin.site. register(MyUser)
