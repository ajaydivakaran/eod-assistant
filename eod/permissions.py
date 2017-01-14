from rest_framework import permissions


class StaffWritePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated() and request.user.is_staff


class TeamEditOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS \
                or request.method == 'POST' \
                or request.user.is_staff:
            return True

        return obj.team.user == request.user
