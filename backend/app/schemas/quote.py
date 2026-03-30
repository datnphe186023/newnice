from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class QuoteRequestBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=8, max_length=20)
    email: Optional[EmailStr] = None
    car_brand: Optional[str] = None
    car_model: Optional[str] = None
    car_year: Optional[int] = None
    film_type_preference: Optional[str] = None
    service_type: Optional[str] = None
    message: Optional[str] = None


class QuoteRequestCreate(QuoteRequestBase):
    pass


class QuoteRequestUpdate(BaseModel):
    status: Optional[str] = None
    admin_notes: Optional[str] = None


class QuoteRequestResponse(QuoteRequestBase):
    id: int
    status: str
    admin_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ContactBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = None
    email: EmailStr
    subject: Optional[str] = None
    message: str = Field(..., min_length=1)


class ContactCreate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
