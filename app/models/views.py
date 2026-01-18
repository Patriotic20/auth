from sqladmin import Admin

from models.role.view import RoleView
from models.user.view import UserView
from models.user_role.view import UserRoleView
from models.role_permission.view import RolePermissionView
from models.permission.view import PermissionView
from models.student.view import StudentView


def register_models(admin: Admin):
    admin.add_view(UserView)
    admin.add_view(RoleView)
    admin.add_view(PermissionView)
    admin.add_view(UserRoleView)
    admin.add_view(RolePermissionView)
    admin.add_view(StudentView)
