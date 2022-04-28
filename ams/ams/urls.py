
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from ams import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('attendance.urls')),
    path('', include('user.urls')),
    path('', include('leave.urls')),
    path('', include('company_calendar.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
