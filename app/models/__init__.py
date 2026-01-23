__all__ = [
    "User",
    "Role",
    "UserRole",
    "RolePermission",
    "Permission",
    "Student",
]


from .permission.model import Permission
from .role.model import Role
from .role_permission.model import RolePermission
from .student.model import Student
from .user.model import User
from .user_role.model import UserRole
