from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from app.utils.sanitize import sanitize_html, sanitize_plain_text


class PostBase(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: Optional[str] = None
    thumbnail: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None

    @field_validator('content', mode='before')
    @classmethod
    def sanitize_content(cls, v: Optional[str]) -> Optional[str]:
        """Sanitize HTML content to prevent XSS."""
        return sanitize_html(v)
    
    @field_validator('excerpt', 'title', 'meta_title', mode='before')
    @classmethod
    def sanitize_text_fields(cls, v: Optional[str]) -> Optional[str]:
        """Sanitize plain text fields."""
        return sanitize_plain_text(v)


class PostCreate(PostBase):
    is_published: bool = False


class PostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    thumbnail: Optional[str] = None
    is_published: Optional[bool] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None

    @field_validator('content', mode='before')
    @classmethod
    def sanitize_content(cls, v: Optional[str]) -> Optional[str]:
        """Sanitize HTML content to prevent XSS."""
        return sanitize_html(v)
    
    @field_validator('excerpt', 'title', 'meta_title', mode='before')
    @classmethod
    def sanitize_text_fields(cls, v: Optional[str]) -> Optional[str]:
        """Sanitize plain text fields."""
        return sanitize_plain_text(v)


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_published: bool
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class PostListResponse(BaseModel):
    """Simplified post for listing"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    slug: str
    excerpt: Optional[str] = None
    thumbnail: Optional[str] = None
    published_at: Optional[datetime] = None
    created_at: datetime
