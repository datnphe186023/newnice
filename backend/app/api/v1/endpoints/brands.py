from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models import Brand
from app.schemas import BrandResponse

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.get("", response_model=List[BrandResponse])
async def get_brands(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get all active brands"""
    query = select(Brand).where(Brand.is_active == True).order_by(Brand.name)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{slug}", response_model=BrandResponse)
async def get_brand(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get single brand by slug"""
    query = select(Brand).where(
        Brand.slug == slug,
        Brand.is_active == True
    )
    
    result = await db.execute(query)
    brand = result.scalar_one_or_none()
    
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    return brand
