from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Allow only Admin role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsStaff(BasePermission):
    """Allow only Staff role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "staff"


class IsMember(BasePermission):
    """Allow only Member role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "member"


class ReadOnly(BasePermission):
    """Allow only GET, HEAD, OPTIONS."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
