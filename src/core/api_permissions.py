from rest_framework import permissions


class IsOwnerOrPublished(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.published and request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
