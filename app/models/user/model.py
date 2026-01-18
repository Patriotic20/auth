from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from models.base import Base
from models.mixins.id_int_pk import IdIntPk
from models.mixins.time_stamp_mixin import TimestampMixin


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.role.model import Role
    from models.user_role.model import UserRole

class User(Base, IdIntPk, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    

    roles: Mapped[list["Role"]] = relationship(
        "Role", 
        secondary="user_roles", 
        back_populates="users", 
        overlaps="user_roles"
    )

    student: Mapped["Student"] = relationship("Student", back_populates="user")

    def __str__(self):
        return self.username
