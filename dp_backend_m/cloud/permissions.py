from rest_framework import permissions


class IsStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_staff:
            return False
        else:
            return True


class IsStaffOrOwnPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        elif not request.user.is_staff:
            return False
        else:
            return True


class IsStaffOrOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        elif not request.user.is_staff:
            return False
        else:
            return True

