from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Profile


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_staff:
            return True

        return obj == request.user


class ModerOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.is_moderator



class IsNotBanned(BasePermission):
    def has_permission(self, request, view):
        return not request.user.profile.is_ban