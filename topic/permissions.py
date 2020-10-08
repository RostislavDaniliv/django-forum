from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_staff:
            return True

        return


class ModerOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.is_moderator


class IsNotBanned(BasePermission):
    def has_permission(self, request, view):
        return not request.user.profile.is_ban


class IsNotMuted(BasePermission):
    def has_permission(self, request, view):
        return not request.user.profile.is_mute


class IsModerHaveTopic(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.moderator == request.user