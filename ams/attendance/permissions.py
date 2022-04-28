from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminUser(permissions.BasePermission):
    message = 'You are not authorized.'

    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.device_id == request.user.device_id
