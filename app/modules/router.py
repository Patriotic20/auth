from fastapi import APIRouter

from .permission.router import router as permission_router
from .role.router import router as role_router
from .user.router import router as user_router

router = APIRouter()

router.include_router(user_router)
router.include_router(role_router)
router.include_router(permission_router)
