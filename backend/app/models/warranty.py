from datetime import date, datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def _uuid() -> str:
    return str(uuid4())


class Dealer(Base):
    __tablename__ = "dealers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    dealer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    activation_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    warranties: Mapped[list["WarrantySerial"]] = relationship("WarrantySerial", back_populates="dealer")


class FilmPackage(Base):
    __tablename__ = "film_packages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    package_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    warranty_duration_months: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    warranties: Mapped[list["WarrantySerial"]] = relationship("WarrantySerial", back_populates="film_package")


class WarrantySerial(Base):
    __tablename__ = "warranty_serials"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    serial: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    qr_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    warranty_type: Mapped[str] = mapped_column(String(30), default="auto_film", nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="unused", nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    activated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    dealer_id: Mapped[Optional[str]] = mapped_column(ForeignKey("dealers.id"), nullable=True)
    customer_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    customer_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    vehicle_plate: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    vehicle_model: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    film_package_id: Mapped[Optional[str]] = mapped_column(ForeignKey("film_packages.id"), nullable=True)
    front_windshield_film_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    rear_windshield_film_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    side_window_film_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    film_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    area_m2: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    install_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    warranty_expiry: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    dealer: Mapped[Optional[Dealer]] = relationship("Dealer", back_populates="warranties")
    film_package: Mapped[Optional[FilmPackage]] = relationship("FilmPackage", back_populates="warranties")
