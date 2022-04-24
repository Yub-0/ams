from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from user.views import MyObtainTokenPairView

from user import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='view all user(admin)'),
    path('users/register', views.RegisterUserView.as_view(), name='register users(all)'),
    path('roles', views.RoleView.as_view(), name='list roles(admin)'),
    path('role/add', views.RegisterRolesView.as_view(), name='register role(admin)'),
    path('role/<int:pk>/', views.RoleDetail.as_view(), name='view specific role'),
    path('departments', views.DepartmentView.as_view(), name='list department(admin)'),
    path('department/add', views.RegisterDepartmentView.as_view(), name='register department(admin)'),
    path('department/<int:pk>/', views.DepartmentDetail.as_view(), name='view specific department'),
    path('user/login/', MyObtainTokenPairView.as_view(), name='user login to generate token(all)'),
    path('user/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='view user details(user-specific)'),
]
