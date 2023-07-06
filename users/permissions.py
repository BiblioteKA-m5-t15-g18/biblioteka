from rest_framework import permissions
from rest_framework.views import Request, View


class IsAccountOnwer(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get("pk")
        return str(request.user.id) == str(user_id)
