from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Category Schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    image: Optional[str] = None
    banner_image: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int = 0
    is_active: bool = True
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    image: Optional[str] = None
    banner_image: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CategoryWithChildren(CategoryResponse):
    children: List["CategoryResponse"] = []


# Brand Schemas
class BrandBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    logo: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    is_active: bool = True


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    logo: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None


class BrandResponse(BrandBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Product Image Schemas
class ProductImageBase(BaseModel):
    image_url: str
    thumbnail_url: Optional[str] = None
    alt_text: Optional[str] = None
    sort_order: int = 0


class ProductImageCreate(ProductImageBase):
    pass


class ProductImageResponse(ProductImageBase):
    id: int
    
    class Config:
        from_attributes = True


# Product Schemas
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sku: Optional[str] = None
    film_code: Optional[str] = None          # e.g. "CR BLK 40", "IR 50", "VR50"
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    price_sedan: Optional[int] = None        # VND
    price_suv: Optional[int] = None          # VND
    is_contact_price: bool = False
    thumbnail: Optional[str] = None
    vlt: Optional[int] = Field(None, ge=0, le=100)
    uv_rejection: Optional[int] = Field(None, ge=0, le=100)
    ir_rejection: Optional[int] = Field(None, ge=0, le=100)
    heat_rejection: Optional[int] = Field(None, ge=0, le=100)
    thickness: Optional[str] = None
    warranty_years: Optional[int] = None
    is_featured: bool = False
    is_active: bool = True
    sort_order: int = 0
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    sku: Optional[str] = None
    film_code: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    price_sedan: Optional[int] = None
    price_suv: Optional[int] = None
    is_contact_price: Optional[bool] = None
    thumbnail: Optional[str] = None
    vlt: Optional[int] = Field(None, ge=0, le=100)
    uv_rejection: Optional[int] = Field(None, ge=0, le=100)
    ir_rejection: Optional[int] = Field(None, ge=0, le=100)
    heat_rejection: Optional[int] = Field(None, ge=0, le=100)
    thickness: Optional[str] = None
    warranty_years: Optional[int] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class ProductResponse(ProductBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    brand: Optional[BrandResponse] = None
    images: List[ProductImageResponse] = []
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    id: int
    name: str
    slug: str
    film_code: Optional[str] = None
    thumbnail: Optional[str] = None
    price_sedan: Optional[int] = None
    price_suv: Optional[int] = None
    is_contact_price: bool
    vlt: Optional[int] = None
    uv_rejection: Optional[int] = None
    heat_rejection: Optional[int] = None
    is_featured: bool
    category: Optional[CategoryResponse] = None
    brand: Optional[BrandResponse] = None
    
    class Config:
        from_attributes = True
