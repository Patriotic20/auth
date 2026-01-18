__all__ = [
    "User",
    "Role",
    "UserRole",
    "RolePermission",
    "Permission",
    "Student",
]


from .user.model import User
from .role.model import Role
from .user_role.model import UserRole
from .role_permission.model import RolePermission
from .permission.model import Permission
from .student.model import Student


