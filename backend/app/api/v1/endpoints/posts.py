from typing import Annotated, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models.content import Post
from app.schemas import PostResponse, PostListResponse, PaginatedResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", response_model=PaginatedResponse[PostListResponse])
async def get_posts(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50)
):
    """Get published posts with pagination"""
    # Count total
    count_query = select(func.count(Post.id)).where(Post.is_published == True)
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Get posts
    query = (
        select(Post)
        .where(Post.is_published == True)
        .order_by(Post.published_at.desc(), Post.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    
    result = await db.execute(query)
    posts = result.scalars().all()
    
    return {
        "items": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }


@router.get("/recent", response_model=List[PostListResponse])
async def get_recent_posts(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = Query(5, ge=1, le=10)
):
    """Get recent published posts"""
    query = (
        select(Post)
        .where(Post.is_published == True)
        .order_by(Post.published_at.desc(), Post.created_at.desc())
        .limit(limit)
    )
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{slug}", response_model=PostResponse)
async def get_post(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get single post by slug"""
    query = select(Post).where(
        Post.slug == slug,
        Post.is_published == True
    )
    
    result = await db.execute(query)
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post
