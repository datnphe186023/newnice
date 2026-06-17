from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings
from app.models import AdminUser
from app.schemas import PasswordChangeRequest, Token, UserLogin, UserCreate, UserResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Login to get access token"""
    result = await db.execute(
        select(AdminUser).where(AdminUser.email == form_data.username)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản đã bị vô hiệu hóa"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()
    
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: Annotated[AdminUser, Depends(get_current_user)]
):
    """Get current user info"""
    return current_user


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    data: PasswordChangeRequest,
    current_user: Annotated[AdminUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Change password for the current admin user"""
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    if data.current_password == data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password"
        )

    current_user.password_hash = get_password_hash(data.new_password)
    current_user.updated_at = datetime.utcnow()
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/register", response_model=UserResponse)
async def register_first_admin(
    data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Register first admin user (only works if no users exist)"""
    # Check if any users exist
    result = await db.execute(select(AdminUser).limit(1))
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin user already exists. Please login."
        )
    
    # Create first admin
    user = AdminUser(
        email=data.email,
        password_hash=get_password_hash(data.password),
        full_name=data.full_name,
        role="super_admin"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user
