from rest_framework import permissions
from app.models import User
"""判断用户有没有该权限"""
class getpermiss(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            mc=User.objects.filter(user=request.data['user']).first()
            if mc.user_type==2:
                return True
        except Exception as e:
            return False
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
