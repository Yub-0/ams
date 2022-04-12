from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from user.views import RegisterUserView, RegisterRolesView, RegisterDepartmentView, RolesView, DepartmentsView, MyObtainTokenPairView, UserListView

from user import views

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
    path('users/', all_user, name='view all user(admin)'),
    path('users/register', reg_user, name='register users(all)'),
    path('roles', list_role, name='list roles(admin)'),
    path('users/roles/register', reg_role, name='register role(admin)'),
    path('departments', list_department, name='list department(admin)'),
    path('users/department/register', reg_department, name='register department(admin)'),
    path('user/login/', MyObtainTokenPairView.as_view(), name='user login to generate token(all)'),
    path('user/refreshToken', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='view user details(user-specific)'),
]