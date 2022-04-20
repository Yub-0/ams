
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('attendance.urls')),
    path('', include('user.urls')),
    path('', include('leave.urls')),
    path('', include('company_calendar.urls'))
]
