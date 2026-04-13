"""
Admin-only posts CRUD endpoints.
All routes require a valid Bearer token (authenticated admin user).
"""
import logging
from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import AdminUser
from app.models.content import Post
from app.schemas import PostResponse, PostListResponse, PaginatedResponse
from app.schemas.post import PostCreate, PostUpdate
from app.api.deps import get_current_user
from slugify import slugify

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["Admin - Posts"])

Db = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[AdminUser, Depends(get_current_user)]


# ---------------------------------------------------------------------------
# List posts (admin — includes drafts)
# ---------------------------------------------------------------------------

@router.get("", response_model=PaginatedResponse[PostResponse])
async def list_posts(
    db: Db,
    _: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    search: Optional[str] = Query(None),
    published: Optional[bool] = Query(None),
):
    """List all posts (including drafts) with search and publish filter."""
    q = select(Post)
    count_q = select(func.count(Post.id))

    if search:
        like = f"%{search}%"
        condition = or_(Post.title.ilike(like), Post.excerpt.ilike(like))
        q = q.where(condition)
        count_q = count_q.where(condition)

    if published is not None:
        q = q.where(Post.is_published == published)
        count_q = count_q.where(Post.is_published == published)

    total = (await db.execute(count_q)).scalar() or 0
    posts = (
        await db.execute(
            q.order_by(Post.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).scalars().all()

    return {
        "items": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, (total + page_size - 1) // page_size),
    }


# ---------------------------------------------------------------------------
# Create post
# ---------------------------------------------------------------------------

@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(data: PostCreate, db: Db, current_user: CurrentUser):
    """Create a new blog post."""
    # Auto-generate slug if not provided
    slug = data.slug or slugify(data.title)

    # Ensure slug is unique
    existing = (await db.execute(select(Post).where(Post.slug == slug))).scalar_one_or_none()
    if existing:
        slug = f"{slug}-{datetime.utcnow().strftime('%H%M%S')}"

    post = Post(
        title=data.title,
        slug=slug,
        excerpt=data.excerpt,
        content=data.content,
        thumbnail=data.thumbnail,
        meta_title=data.meta_title,
        meta_description=data.meta_description,
        is_published=data.is_published,
        published_at=datetime.utcnow() if data.is_published else None,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    logger.info("Post created: %s (id=%d) by %s", post.slug, post.id, current_user.email)
    return post


# ---------------------------------------------------------------------------
# Get single post
# ---------------------------------------------------------------------------

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Db, _: CurrentUser):
    """Get a single post by ID (admin — no published filter)."""
    post = (await db.execute(select(Post).where(Post.id == post_id))).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


# ---------------------------------------------------------------------------
# Update post
# ---------------------------------------------------------------------------

@router.patch("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, data: PostUpdate, db: Db, current_user: CurrentUser):
    """Partially update a post."""
    post = (await db.execute(select(Post).where(Post.id == post_id))).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    update_data = data.model_dump(exclude_unset=True)

    # Handle slug uniqueness if changed
    if "slug" in update_data and update_data["slug"] != post.slug:
        conflict = (
            await db.execute(select(Post).where(Post.slug == update_data["slug"], Post.id != post_id))
        ).scalar_one_or_none()
        if conflict:
            raise HTTPException(status_code=400, detail="Slug này đã được sử dụng bởi bài viết khác")

    # Set published_at when first publishing
    if update_data.get("is_published") and not post.is_published:
        update_data["published_at"] = datetime.utcnow()
    elif update_data.get("is_published") is False:
        update_data["published_at"] = None

    for key, value in update_data.items():
        setattr(post, key, value)

    post.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(post)
    logger.info("Post updated: %s (id=%d) by %s", post.slug, post.id, current_user.email)
    return post


# ---------------------------------------------------------------------------
# Delete post
# ---------------------------------------------------------------------------

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Db, current_user: CurrentUser):
    """Delete a post permanently."""
    post = (await db.execute(select(Post).where(Post.id == post_id))).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await db.delete(post)
    await db.commit()
    logger.info("Post deleted: id=%d by %s", post_id, current_user.email)
