from accounts.permissions import RolePermission
from core.choices import UserRole


class OrganizationManagePermission(RolePermission):
    allowed_roles = (
        UserRole.SYSTEM_ADMIN,
        UserRole.UNIVERSITY_ADMIN,
        UserRole.FACULTY_ADMIN,
    )
