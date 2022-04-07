from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import RegisterUserView, RegisterRolesView, RegisterDepartmentView, RolesView, DepartmentsView, MyObtainTokenPairView, UserListView

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
all_user = UserListView.as_view({
    'get': 'list',
})
urlpatterns =[
    path('users/', all_user, name='all_user'),
    path('users/register', reg_user, name='reg_user'),
    path('users/roles/register', reg_role, name='reg_role'),
    path('users/department/register', reg_department, name='reg_department'),
    path('roles', list_role, name='list_role'),
    path('departments', list_department, name='list_department'),
    # path('user/login', views.UserLogin.as_view(), name='loginUser'),
    path('user/generateToken/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('user/refreshToken', TokenRefreshView.as_view(), name='token_refresh'),
]