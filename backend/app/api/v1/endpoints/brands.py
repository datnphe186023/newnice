from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from slugify import slugify

from app.core.database import get_db
from app.models import Brand, AdminUser
from app.schemas import BrandResponse, BrandCreate, BrandUpdate, MessageResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/brands", tags=["Brands"])


async def _build_unique_slug(db: AsyncSession, name: str, exclude_id: int | None = None) -> str:
    base_slug = slugify(name)
    slug = base_slug
    counter = 1

    while True:
        query = select(Brand).where(Brand.slug == slug)
        if exclude_id is not None:
            query = query.where(Brand.id != exclude_id)
        existing = (await db.execute(query)).scalar_one_or_none()
        if not existing:
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


@router.get("", response_model=List[BrandResponse])
async def get_brands(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get all active brands"""
    query = select(Brand).where(Brand.is_active == True).order_by(Brand.name)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/admin/all", response_model=List[BrandResponse])
async def admin_get_brands(
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AdminUser, Depends(get_current_user)],
):
    query = select(Brand).order_by(Brand.name)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("", response_model=BrandResponse, status_code=201)
async def create_brand(
    data: BrandCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AdminUser, Depends(get_current_user)],
):
    brand = Brand(**data.model_dump(), slug=await _build_unique_slug(db, data.name))
    db.add(brand)
    await db.commit()
    await db.refresh(brand)
    return brand


@router.put("/{brand_id}", response_model=BrandResponse)
async def update_brand(
    brand_id: int,
    data: BrandUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AdminUser, Depends(get_current_user)],
):
    brand = (await db.execute(select(Brand).where(Brand.id == brand_id))).scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    update_data = data.model_dump(exclude_unset=True)
    if "name" in update_data and update_data["name"] and update_data["name"] != brand.name:
        update_data["slug"] = await _build_unique_slug(db, update_data["name"], exclude_id=brand_id)

    for field, value in update_data.items():
        setattr(brand, field, value)

    await db.commit()
    await db.refresh(brand)
    return brand


@router.delete("/{brand_id}", response_model=MessageResponse)
async def delete_brand(
    brand_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AdminUser, Depends(get_current_user)],
):
    brand = (await db.execute(select(Brand).where(Brand.id == brand_id))).scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    await db.delete(brand)
    await db.commit()
    return MessageResponse(message="Brand deleted", success=True)


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
