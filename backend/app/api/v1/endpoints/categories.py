from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models import Category
from app.schemas import CategoryResponse, CategoryWithChildren

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=List[CategoryWithChildren])
async def get_categories(
    db: Annotated[AsyncSession, Depends(get_db)],
    include_inactive: bool = False
):
    """Get all categories with their children (tree structure)"""
    query = select(Category).where(Category.parent_id == None)
    
    if not include_inactive:
        query = query.where(Category.is_active == True)
    
    query = query.options(selectinload(Category.children)).order_by(Category.sort_order)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{slug}", response_model=CategoryResponse)
async def get_category(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get single category by slug"""
    query = select(Category).where(
        Category.slug == slug,
        Category.is_active == True
    )
    
    result = await db.execute(query)
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category
