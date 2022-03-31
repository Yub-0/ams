from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from user.views import RegisterUserView, RegisterRolesView, RegisterDepartmentView, RolesView, DepartmentsView

reg_user = RegisterUserView.as_view({
    'post': 'create',
})
reg_role = RegisterRolesView.as_view({
    'post': 'create',
})
reg_department = RegisterDepartmentView.as_view({
    'post': 'create',
})
list_role = RolesView.as_view({
    'get': 'list',
})
list_department = DepartmentsView.as_view({
    'get': 'list',
})
urlpatterns = format_suffix_patterns([
    path('users/register', reg_user, name='reg_user'),
    path('users/roles/register', reg_role, name='reg_role'),
    path('users/department/register', reg_department, name='reg_department'),
    path('roles', list_role, name='list_role'),
    path('departments', list_department, name='list_department')
])