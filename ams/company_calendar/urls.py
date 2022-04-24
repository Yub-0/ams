
from django.urls import path
from company_calendar.views import CreateHolidays, ViewHolidays

add_holiday = CreateHolidays.as_view({
    'post': 'create'
})
view_holiday = ViewHolidays.as_view({
    'get': 'list'
})
urlpatterns = [
    path('addHoliday', add_holiday, name='Add Holiday in company calendar'),
    path('viewHolidays', view_holiday, name='View Holidays')
]