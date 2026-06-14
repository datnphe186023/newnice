from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class DealerBase(BaseModel):
    dealer_name: str = Field(..., min_length=1, max_length=255)
    activation_code: str = Field(..., min_length=3, max_length=100)
    status: str = "active"


class DealerCreate(DealerBase):
    pass


class DealerUpdate(BaseModel):
    dealer_name: Optional[str] = None
    activation_code: Optional[str] = None
    status: Optional[str] = None


class DealerResponse(DealerBase):
    id: str
    serial_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FilmPackageBase(BaseModel):
    package_name: str = Field(..., min_length=1, max_length=255)
    warranty_duration_months: int = Field(..., ge=1, le=240)
    status: str = "active"


class FilmPackageCreate(FilmPackageBase):
    pass


class FilmPackageUpdate(BaseModel):
    package_name: Optional[str] = None
    warranty_duration_months: Optional[int] = Field(None, ge=1, le=240)
    status: Optional[str] = None


class FilmPackageResponse(FilmPackageBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WarrantyActivationCreate(BaseModel):
    vehicle_plate: str = Field(..., min_length=1, max_length=30)
    vehicle_model: str = Field(..., min_length=1, max_length=255)
    customer_phone: str = Field(..., min_length=8, max_length=20)
    customer_name: str = Field(..., min_length=1, max_length=255)
    film_package_id: str
    front_windshield_film_code: str = Field(..., min_length=1, max_length=100)
    rear_windshield_film_code: str = Field(..., min_length=1, max_length=100)
    side_window_film_code: str = Field(..., min_length=1, max_length=100)
    install_date: date
    activation_code: str = Field(..., min_length=3, max_length=100)


class WarrantyPublicInfo(BaseModel):
    customer_name: str
    customer_phone: str
    vehicle_plate: str
    vehicle_model: str
    film_package: str
    install_date: date
    warranty_expiry: date


class WarrantyLookupResponse(BaseModel):
    serial: str
    status: str
    warranty: Optional[WarrantyPublicInfo] = None
    film_packages: list[FilmPackageResponse] = []


class WarrantyAdminUpdate(BaseModel):
    status: Optional[str] = None
    dealer_id: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    vehicle_plate: Optional[str] = None
    vehicle_model: Optional[str] = None
    film_package_id: Optional[str] = None
    front_windshield_film_code: Optional[str] = None
    rear_windshield_film_code: Optional[str] = None
    side_window_film_code: Optional[str] = None
    install_date: Optional[date] = None
    warranty_expiry: Optional[date] = None


class WarrantyAdminResponse(BaseModel):
    id: str
    serial: str
    qr_url: Optional[str]
    status: str
    created_at: datetime
    activated_at: Optional[datetime]
    dealer_id: Optional[str]
    dealer_name: Optional[str]
    customer_name: Optional[str]
    customer_phone: Optional[str]
    vehicle_plate: Optional[str]
    vehicle_model: Optional[str]
    film_package_id: Optional[str]
    film_package_name: Optional[str]
    front_windshield_film_code: Optional[str]
    rear_windshield_film_code: Optional[str]
    side_window_film_code: Optional[str]
    install_date: Optional[date]
    warranty_expiry: Optional[date]


class SerialGenerateRequest(BaseModel):
    count: int = Field(..., ge=1, le=1000)
    prefix: str = Field("DLA", min_length=1, max_length=12)
    dealer_id: str = Field(..., min_length=1, max_length=36)
    qr_base_url: Optional[str] = Field(None, max_length=500)


class SerialGenerateResponse(BaseModel):
    items: list[WarrantyAdminResponse]
