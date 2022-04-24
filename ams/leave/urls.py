from leave.views import UserLeave
from django.urls import path

from leave.views import ViewLeave

create_leave = UserLeave.as_view({
    'post': 'create'
})
check_leave = ViewLeave.as_view({
    'get': 'list'
})
urlpatterns = [
    path('createLeave', create_leave),
    path('checkLeave', check_leave)
]