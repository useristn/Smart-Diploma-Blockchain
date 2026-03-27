from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework.permissions import BasePermission

from core.choices import UserRole


def has_any_role(user, roles):
    return bool(
        user
        and user.is_authenticated
        and (user.role in roles or user.role == UserRole.SYSTEM_ADMIN)
    )


class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = ()

    def test_func(self):
        return has_any_role(self.request.user, self.allowed_roles)


class RolePermission(BasePermission):
    allowed_roles = ()

    def has_permission(self, request, view):
        return has_any_role(request.user, self.allowed_roles)
