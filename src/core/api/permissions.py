from rest_framework import permissions


class IsOwnerOrSafeMethods(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True

        return False
