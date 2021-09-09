from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user and request.user.is_staff:
            return True
        return False


class SelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj.id == request.user.id:
            return True
        return False
