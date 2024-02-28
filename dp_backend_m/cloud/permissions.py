from rest_framework import permissions


class IsStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        if not request.user.if_staff:
            return False
        else:
            return True


class IsStaffOrOwnPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user)
        if request.user == obj:
            return True
        elif not request.user.is_staff:
            return False
        else:
            return True


class IsStaffOrOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user)
        if request.user == obj.owner:
            return True
        elif not request.user.is_staff:
            return False
        else:
            return True

