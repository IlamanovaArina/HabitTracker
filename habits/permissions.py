from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """ Разрешение для владельца объекта """
    def has_object_permission(self, request, view, obj):
        if obj.user is not None:
            if obj.user == request.user:
                return True
            return False
        if obj.owner is not None:
            if obj.owner == request.user:
                return True
            return False
