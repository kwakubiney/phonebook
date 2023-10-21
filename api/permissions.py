from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'GET':
            return True
        return request.user and request.user.is_staff

class IsDeleteAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.method == 'DELETE' or request.method == "PATCH") and not request.user.is_staff:
            return False
        return True