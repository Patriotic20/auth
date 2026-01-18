from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import Integer, ForeignKey

from models.base import Base
from models.mixins.id_int_pk import IdIntPk
from models.mixins.time_stamp_mixin import TimestampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.role.model import Role
    from models.permission.model import Permission

class RolePermission(Base, IdIntPk, TimestampMixin):
    __tablename__ = "role_permissions"

    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id: Mapped[int] = mapped_column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)


    role: Mapped["Role"] = relationship("Role", lazy="selectin")
    permission: Mapped["Permission"] = relationship("Permission", lazy="selectin")
    

    def __str__(self) -> str:
        return f"{self.role} → {self.permission}"