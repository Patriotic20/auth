from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt
from jwt import PyJWTError

from core.config import settings
from models.user.model import User
from models.role.model import Role
from models.permission.model import Permission
from models.user_role.model import UserRole
from models.role_permission.model import RolePermission
from core.db_helper import db_helper

# Используем заголовок Authorization
api_key_header = APIKeyHeader(name="Authorization")

async def get_current_user_id(token: str = Depends(api_key_header)):
    # Если токен приходит как "Bearer <token>", нужно убрать префикс
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")
    
    try:
        payload = jwt.decode(
            token, 
            settings.jwt.access_token_secret, 
            algorithms=[settings.jwt.algorithm]
        )
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token: user_id missing"
            )
        return user_id
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate credentials"
        )

class PermissionRequired:
    def __init__(self, permission_name: str):
        self.permission_name = permission_name

    async def __call__(
        self, 
        user_id: int = Depends(get_current_user_id), 
        session: AsyncSession = Depends(db_helper.session_getter)
    ) -> User:  # Теперь возвращаем модель User
        
        # 1. Проверяем существование разрешения и создаем, если его нет
        perm_stmt = select(Permission).where(Permission.name == self.permission_name)
        perm_result = await session.execute(perm_stmt)
        perm_obj = perm_result.scalar_one_or_none()

        if not perm_obj:
            perm_obj = Permission(name=self.permission_name)
            session.add(perm_obj)
            await session.commit()
            await session.refresh(perm_obj)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{self.permission_name}' created. Assign it to a role."
            )

        # 2. Проверяем наличие права у пользователя И загружаем данные пользователя
        # Используем JOIN для проверки, но выбираем (select) саму сущность User
        stmt = (
            select(User)
            .join(UserRole)
            .join(Role)
            .join(RolePermission)
            .join(Permission)
            .where(
                User.id == user_id,
                Permission.name == self.permission_name
            )
        )
        
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: user lacks '{self.permission_name}' permission"
            )
        
        return user