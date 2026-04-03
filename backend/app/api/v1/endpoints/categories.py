from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models import Category, AdminUser
from app.schemas import CategoryResponse, CategoryWithChildren, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


def generate_slug(name: str) -> str:
    """Generate a URL-friendly slug from name."""
    import re
    import unicodedata
    
    # Normalize unicode characters
    slug = unicodedata.normalize('NFKD', name)
    slug = slug.encode('ascii', 'ignore').decode('ascii')
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug.lower())
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    return slug


# ================== Public Routes ==================

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


# ================== Admin Routes ==================

@router.get("/admin/all", response_model=List[CategoryWithChildren])
async def admin_get_all_categories(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[AdminUser, Depends(get_current_user)],
):
    """Admin: Get all categories including inactive ones"""
    query = (
        select(Category)
        .where(Category.parent_id == None)
        .options(selectinload(Category.children))
        .order_by(Category.sort_order)
    )
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/admin/{category_id}", response_model=CategoryResponse)
async def admin_get_category(
    category_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[AdminUser, Depends(get_current_user)],
):
    """Admin: Get category by ID"""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category


@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[AdminUser, Depends(get_current_user)],
):
    """Admin: Create a new category"""
    # Generate slug
    base_slug = generate_slug(data.name)
    slug = base_slug
    
    # Check for duplicate slug and make unique if needed
    counter = 1
    while True:
        result = await db.execute(select(Category).where(Category.slug == slug))
        if not result.scalar_one_or_none():
            break
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    # Validate parent_id if provided
    if data.parent_id:
        result = await db.execute(select(Category).where(Category.id == data.parent_id))
        parent = result.scalar_one_or_none()
        if not parent:
            raise HTTPException(status_code=400, detail="Parent category not found")
    
    # Create category
    category = Category(
        **data.model_dump(),
        slug=slug,
    )
    
    db.add(category)
    await db.commit()
    await db.refresh(category)
    
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[AdminUser, Depends(get_current_user)],
):
    """Admin: Update a category"""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Validate parent_id if being changed
    if data.parent_id is not None:
        if data.parent_id == category_id:
            raise HTTPException(status_code=400, detail="Category cannot be its own parent")
        
        if data.parent_id != 0:  # 0 means set to root
            result = await db.execute(select(Category).where(Category.id == data.parent_id))
            parent = result.scalar_one_or_none()
            if not parent:
                raise HTTPException(status_code=400, detail="Parent category not found")
            
            # Check for circular reference
            current_parent_id = data.parent_id
            while current_parent_id:
                if current_parent_id == category_id:
                    raise HTTPException(status_code=400, detail="Circular reference detected")
                result = await db.execute(select(Category).where(Category.id == current_parent_id))
                current_parent = result.scalar_one_or_none()
                current_parent_id = current_parent.parent_id if current_parent else None
    
    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    
    # If parent_id is 0, set to None (root level)
    if update_data.get('parent_id') == 0:
        update_data['parent_id'] = None
    
    # Regenerate slug if name changed
    if 'name' in update_data and update_data['name'] != category.name:
        base_slug = generate_slug(update_data['name'])
        slug = base_slug
        counter = 1
        while True:
            result = await db.execute(
                select(Category).where(Category.slug == slug, Category.id != category_id)
            )
            if not result.scalar_one_or_none():
                break
            slug = f"{base_slug}-{counter}"
            counter += 1
        update_data['slug'] = slug
    
    for field, value in update_data.items():
        setattr(category, field, value)
    
    await db.commit()
    await db.refresh(category)
    
    return category


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[AdminUser, Depends(get_current_user)],
):
    """Admin: Delete a category"""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has children
    result = await db.execute(select(func.count()).select_from(Category).where(Category.parent_id == category_id))
    children_count = result.scalar()
    
    if children_count > 0:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete category with subcategories. Delete subcategories first."
        )
    
    # Check if category has products
    from app.models import Product
    result = await db.execute(select(func.count()).select_from(Product).where(Product.category_id == category_id))
    products_count = result.scalar()
    
    if products_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete category with {products_count} product(s). Reassign or delete products first."
        )
    
    await db.delete(category)
    await db.commit()
    
    return {"success": True, "message": "Category deleted"}


@router.put("/admin/reorder", response_model=List[CategoryResponse])
async def reorder_categories(
    order: List[dict],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[AdminUser, Depends(get_current_user)],
):
    """
    Admin: Reorder categories (batch update sort_order).
    
    Expects a list of objects with 'id' and 'sort_order' fields:
    [{"id": 1, "sort_order": 0}, {"id": 2, "sort_order": 1}, ...]
    """
    updated_categories = []
    
    for item in order:
        category_id = item.get('id')
        sort_order = item.get('sort_order')
        
        if category_id is None or sort_order is None:
            continue
        
        result = await db.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        
        if category:
            category.sort_order = sort_order
            updated_categories.append(category)
    
    await db.commit()
    
    # Refresh all updated categories
    for cat in updated_categories:
        await db.refresh(cat)
    
    return updated_categories
