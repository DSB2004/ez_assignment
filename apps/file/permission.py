from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from apps.user.models import Role

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.email is None or request.role is None:
            raise PermissionDenied(detail="Authentication credentials were not provided.")
        return True

class IsOperationUser(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request, 'role') or request.role != Role.OPERATION:
            raise PermissionDenied(detail="Only operation users can access this endpoint.")
        return True

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request, 'role') or request.role != Role.CLIENT:
            raise PermissionDenied(detail="Only client users can access this endpoint.")
        return True
