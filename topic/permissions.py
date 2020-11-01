from rest_framework import permissions
from rest_framework.permissions import BasePermission

# Access class for admins and creators, otherwise read-only


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_staff:
            return True

        return


# Access class for moderators


class ModerOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.is_moderator


# Access class for not banned users


class IsNotBanned(BasePermission):
    def has_permission(self, request, view):
        return not request.user.profile.is_ban


# Access class for not Muted users


class IsNotMuted(BasePermission):
    def has_permission(self, request, view):
        return not request.user.profile.is_mute


# Access class for moderators to whom the topic is assigned


class IsModerHaveTopic(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.moderator == request.user