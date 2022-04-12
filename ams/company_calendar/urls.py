
from django.urls import path
from company_calendar.views import CreateHolidays


add_holiday = CreateHolidays.as_view({
    'post': 'create'
})
urlpatterns = [
    path('addHolidays', add_holiday, name='Add Holiday in company calendar' )
]