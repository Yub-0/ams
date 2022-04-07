from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_admin


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user

        # Write permissions are only allowed to the owner of the snippet.
        return False


class IsUser(BasePermission):
   def has_permission(self, request, view):
      return request.user.is_user


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.device_id == request.user