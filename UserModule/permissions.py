from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True

        if hasattr(obj, 'customer'):
            return obj.customer == request.user

        if hasattr(obj, 'ticket') and hasattr(obj.ticket, 'customer'):
            return obj.ticket.customer == request.user

        return False
