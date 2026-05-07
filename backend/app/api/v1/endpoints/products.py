from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from slugify import slugify

from app.core.database import get_db
from app.models import Product, Category, Brand, AdminUser
from app.schemas import ProductResponse, ProductListResponse, PaginatedResponse, ProductCreate, ProductUpdate, MessageResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


async def _ensure_category_brand_exist(db: AsyncSession, category_id: Optional[int], brand_id: Optional[int]) -> None:
    if category_id is not None:
        category = (await db.execute(select(Category).where(Category.id == category_id))).scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")

    if brand_id is not None:
        brand = (await db.execute(select(Brand).where(Brand.id == brand_id))).scalar_one_or_none()
        if not brand:
            raise HTTPException(status_code=400, detail="Brand not found")


async def _build_unique_slug(db: AsyncSession, name: str, exclude_id: Optional[int] = None) -> str:
    base_slug = slugify(name)
    slug = base_slug
    counter = 1

    while True:
        query = select(Product).where(Product.slug == slug)
        if exclude_id is not None:
            query = query.where(Product.id != exclude_id)
        exists = (await db.execute(query)).scalar_one_or_none()
        if not exists:
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


@router.get("", response_model=PaginatedResponse[ProductListResponse])
async def get_products(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    category_slug: Optional[str] = None,
    brand_slug: Optional[str] = None,
    film_type: Optional[str] = None,
    vlt_min: Optional[int] = Query(None, ge=0, le=100),
    vlt_max: Optional[int] = Query(None, ge=0, le=100),
    is_featured: Optional[bool] = None,
    search: Optional[str] = None,
):
    """Get paginated list of products with filters"""
    query = select(Product).where(Product.is_active == True)
    count_query = select(func.count(Product.id)).where(Product.is_active == True)
    
    # Apply filters
    if category_slug:
        category = await db.execute(select(Category).where(Category.slug == category_slug))
        cat = category.scalar_one_or_none()
        if cat:
            query = query.where(Product.category_id == cat.id)
            count_query = count_query.where(Product.category_id == cat.id)
    
    if brand_slug:
        brand = await db.execute(select(Brand).where(Brand.slug == brand_slug))
        br = brand.scalar_one_or_none()
        if br:
            query = query.where(Product.brand_id == br.id)
            count_query = count_query.where(Product.brand_id == br.id)
    
    if film_type:
        query = query.where(Product.film_type == film_type)
        count_query = count_query.where(Product.film_type == film_type)
    
    if vlt_min is not None:
        query = query.where(Product.vlt >= vlt_min)
        count_query = count_query.where(Product.vlt >= vlt_min)
    
    if vlt_max is not None:
        query = query.where(Product.vlt <= vlt_max)
        count_query = count_query.where(Product.vlt <= vlt_max)
    
    if is_featured is not None:
        query = query.where(Product.is_featured == is_featured)
        count_query = count_query.where(Product.is_featured == is_featured)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(Product.name.ilike(search_term))
        count_query = count_query.where(Product.name.ilike(search_term))
    
    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination and ordering
    query = query.options(
        selectinload(Product.category),
        selectinload(Product.brand)
    ).order_by(Product.sort_order, Product.created_at.desc())
    
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    result = await db.execute(query)
    products = result.scalars().all()
    
    total_pages = (total + page_size - 1) // page_size
    
    return PaginatedResponse(
        items=products,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AdminUser, Depends(get_current_user)],
):
    await _ensure_category_brand_exist(db, data.category_id, data.brand_id)

    payload = data.model_dump()
    product = Product(**payload, slug=await _build_unique_slug(db, data.name))
    db.add(product)
    await db.commit()
    await db.refresh(product)

    loaded = (
        await db.execute(
            select(Product)
            .where(Product.id == product.id)
            .options(selectinload(Product.category), selectinload(Product.brand), selectinload(Product.images))
        )
    ).scalar_one()
    return loaded


@router.get("/admin/{product_id}", response_model=ProductResponse)
async def admin_get_product_by_id(
    product_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AdminUser, Depends(get_current_user)],
):
    product = (
        await db.execute(
            select(Product)
            .where(Product.id == product_id)
            .options(selectinload(Product.category), selectinload(Product.brand), selectinload(Product.images))
        )
    ).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AdminUser, Depends(get_current_user)],
):
    product = (await db.execute(select(Product).where(Product.id == product_id))).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = data.model_dump(exclude_unset=True)
    await _ensure_category_brand_exist(db, update_data.get("category_id"), update_data.get("brand_id"))

    if "name" in update_data and update_data["name"] and update_data["name"] != product.name:
        update_data["slug"] = await _build_unique_slug(db, update_data["name"], exclude_id=product_id)

    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    loaded = (
        await db.execute(
            select(Product)
            .where(Product.id == product.id)
            .options(selectinload(Product.category), selectinload(Product.brand), selectinload(Product.images))
        )
    ).scalar_one()
    return loaded


@router.delete("/{product_id}", response_model=MessageResponse)
async def delete_product(
    product_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AdminUser, Depends(get_current_user)],
):
    product = (await db.execute(select(Product).where(Product.id == product_id))).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()
    return MessageResponse(message="Product deleted", success=True)


@router.get("/featured", response_model=List[ProductListResponse])
async def get_featured_products(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = Query(8, ge=1, le=20)
):
    """Get featured products for homepage"""
    query = select(Product).where(
        Product.is_active == True,
        Product.is_featured == True
    ).options(
        selectinload(Product.category),
        selectinload(Product.brand)
    ).order_by(Product.sort_order).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{slug}", response_model=ProductResponse)
async def get_product(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get single product by slug"""
    query = select(Product).where(
        Product.slug == slug,
        Product.is_active == True
    ).options(
        selectinload(Product.category),
        selectinload(Product.brand),
        selectinload(Product.images)
    )
    
    result = await db.execute(query)
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product
