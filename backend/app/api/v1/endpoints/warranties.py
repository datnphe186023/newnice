import csv
import io
import secrets
import string
from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import AdminUser, Dealer, FilmPackage, WarrantySerial
from app.schemas import (
    DealerCreate,
    DealerResponse,
    DealerUpdate,
    FilmPackageCreate,
    FilmPackageResponse,
    FilmPackageUpdate,
    PaginatedResponse,
    SerialGenerateRequest,
    SerialGenerateResponse,
    WarrantyActivationCreate,
    WarrantyAdminResponse,
    WarrantyAdminUpdate,
    WarrantyLookupResponse,
)
from app.schemas.warranty import WarrantyPublicInfo

router = APIRouter(tags=["Warranty"])

Db = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[AdminUser, Depends(get_current_user)]

VALID_SERIAL_STATUSES = {"unused", "activated", "expired", "void"}
VALID_ACTIVE_STATUSES = {"active", "inactive"}
VALID_WARRANTY_TYPES = {"auto_film", "auto_ppf", "building_film", "kitchen_ppf"}
VEHICLE_WARRANTY_TYPES = {"auto_film", "auto_ppf"}
AREA_WARRANTY_TYPES = {"building_film", "kitchen_ppf"}
ALPHABET = string.ascii_uppercase + string.digits


def _normalize_serial(serial: str) -> str:
    return serial.strip().upper()


def _normalize_code(code: str) -> str:
    return code.strip()


def _warranty_type(row: WarrantySerial) -> str:
    return row.warranty_type or "auto_film"


def _require_text(value: str | None, detail: str) -> str:
    if not value or not value.strip():
        raise HTTPException(status_code=400, detail=detail)
    return value.strip()


def _add_months(value: date, months: int) -> date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    month_lengths = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day = min(value.day, month_lengths[month - 1])
    return date(year, month, day)


def _serialize_warranty(row: WarrantySerial) -> WarrantyAdminResponse:
    return WarrantyAdminResponse(
        id=row.id,
        serial=row.serial,
        qr_url=row.qr_url,
        warranty_type=_warranty_type(row),
        status=row.status,
        created_at=row.created_at,
        activated_at=row.activated_at,
        dealer_id=row.dealer_id,
        dealer_name=row.dealer.dealer_name if row.dealer else None,
        customer_name=row.customer_name,
        customer_phone=row.customer_phone,
        vehicle_plate=row.vehicle_plate,
        vehicle_model=row.vehicle_model,
        film_package_id=row.film_package_id,
        film_package_name=row.film_package.package_name if row.film_package else None,
        front_windshield_film_code=row.front_windshield_film_code,
        rear_windshield_film_code=row.rear_windshield_film_code,
        side_window_film_code=row.side_window_film_code,
        film_code=row.film_code,
        area_m2=row.area_m2,
        install_date=row.install_date,
        warranty_expiry=row.warranty_expiry,
    )


def _make_public_info(row: WarrantySerial) -> WarrantyPublicInfo:
    warranty_type = _warranty_type(row)
    if not (row.customer_name and row.customer_phone and row.install_date):
        raise HTTPException(status_code=409, detail="Warranty data is incomplete")

    if warranty_type in VEHICLE_WARRANTY_TYPES and not (
        row.vehicle_plate
        and row.vehicle_model
        and row.film_package
        and row.front_windshield_film_code
        and row.rear_windshield_film_code
        and row.side_window_film_code
        and row.warranty_expiry
    ):
        raise HTTPException(status_code=409, detail="Warranty data is incomplete")

    if warranty_type in AREA_WARRANTY_TYPES and not (row.film_code and row.area_m2):
        raise HTTPException(status_code=409, detail="Warranty data is incomplete")

    return WarrantyPublicInfo(
        warranty_type=warranty_type,
        customer_name=row.customer_name,
        customer_phone=row.customer_phone,
        vehicle_plate=row.vehicle_plate,
        vehicle_model=row.vehicle_model,
        film_package=row.film_package.package_name if row.film_package else None,
        front_windshield_film_code=row.front_windshield_film_code,
        rear_windshield_film_code=row.rear_windshield_film_code,
        side_window_film_code=row.side_window_film_code,
        film_code=row.film_code,
        area_m2=row.area_m2,
        install_date=row.install_date,
        warranty_expiry=row.warranty_expiry,
    )


async def _get_warranty_by_serial(db: AsyncSession, serial: str) -> WarrantySerial:
    row = (
        await db.execute(
            select(WarrantySerial)
            .options(selectinload(WarrantySerial.dealer), selectinload(WarrantySerial.film_package))
            .where(WarrantySerial.serial == _normalize_serial(serial))
            .execution_options(populate_existing=True)
        )
    ).scalar_one_or_none()

    if not row:
        raise HTTPException(status_code=404, detail="Serial not found")
    return row


async def _active_packages(db: AsyncSession) -> list[FilmPackage]:
    return (
        await db.execute(
            select(FilmPackage)
            .where(FilmPackage.status == "active")
            .order_by(FilmPackage.warranty_duration_months)
        )
    ).scalars().all()


def _generate_serial(prefix: str) -> str:
    safe_prefix = "".join(ch for ch in prefix.upper() if ch.isalnum())[:12] or "DLA"
    left = "".join(secrets.choice(ALPHABET) for _ in range(4))
    right = "".join(secrets.choice(ALPHABET) for _ in range(4))
    return f"{safe_prefix}-{left}-{right}"


@router.get("/warranties/{serial}", response_model=WarrantyLookupResponse)
async def lookup_warranty(serial: str, db: Db):
    row = await _get_warranty_by_serial(db, serial)

    if row.status == "unused":
        packages = await _active_packages(db)
        return WarrantyLookupResponse(
            serial=row.serial,
            warranty_type=_warranty_type(row),
            status=row.status,
            film_packages=packages,
        )

    if row.status == "activated":
        return WarrantyLookupResponse(
            serial=row.serial,
            warranty_type=_warranty_type(row),
            status=row.status,
            warranty=_make_public_info(row),
        )

    return WarrantyLookupResponse(serial=row.serial, warranty_type=_warranty_type(row), status=row.status)


@router.post("/warranties/{serial}/activate", response_model=WarrantyLookupResponse)
async def activate_warranty(serial: str, payload: WarrantyActivationCreate, db: Db):
    row = await _get_warranty_by_serial(db, serial)

    if row.status != "unused":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Serial has already been used")

    dealer = (
        await db.execute(
            select(Dealer).where(
                Dealer.activation_code == _normalize_code(payload.activation_code),
                Dealer.status == "active",
            )
        )
    ).scalar_one_or_none()
    if not dealer:
        raise HTTPException(status_code=400, detail="Invalid dealer activation code")
    if row.dealer_id and row.dealer_id != dealer.id:
        raise HTTPException(status_code=400, detail="Dealer activation code does not match this serial")

    warranty_type = _warranty_type(row)
    if payload.warranty_type and payload.warranty_type != warranty_type:
        raise HTTPException(status_code=400, detail="Warranty type does not match this serial")

    package = None
    if warranty_type in VEHICLE_WARRANTY_TYPES:
        vehicle_plate = _require_text(payload.vehicle_plate, "Vehicle plate is required")
        vehicle_model = _require_text(payload.vehicle_model, "Vehicle model is required")
        front_code = _require_text(payload.front_windshield_film_code, "Front windshield film code is required")
        rear_code = _require_text(payload.rear_windshield_film_code, "Rear windshield film code is required")
        side_code = _require_text(payload.side_window_film_code, "Side window film code is required")
        if not payload.film_package_id:
            raise HTTPException(status_code=400, detail="Invalid film package")

        package = (
            await db.execute(
                select(FilmPackage).where(
                    FilmPackage.id == payload.film_package_id,
                    FilmPackage.status == "active",
                )
            )
        ).scalar_one_or_none()
        if not package:
            raise HTTPException(status_code=400, detail="Invalid film package")
    else:
        film_code = _require_text(payload.film_code, "Film code is required")
        if payload.area_m2 is None or payload.area_m2 <= 0:
            raise HTTPException(status_code=400, detail="Area is required")

    row.status = "activated"
    row.activated_at = datetime.utcnow()
    row.dealer_id = dealer.id
    row.dealer = dealer
    row.customer_name = payload.customer_name.strip()
    row.customer_phone = payload.customer_phone.strip()
    row.install_date = payload.install_date

    if warranty_type in VEHICLE_WARRANTY_TYPES and package:
        row.vehicle_plate = vehicle_plate.upper()
        row.vehicle_model = vehicle_model
        row.film_package_id = package.id
        row.film_package = package
        row.front_windshield_film_code = front_code
        row.rear_windshield_film_code = rear_code
        row.side_window_film_code = side_code
        row.film_code = None
        row.area_m2 = None
        row.warranty_expiry = _add_months(payload.install_date, package.warranty_duration_months)
    else:
        row.vehicle_plate = None
        row.vehicle_model = None
        row.film_package_id = None
        row.film_package = None
        row.front_windshield_film_code = None
        row.rear_windshield_film_code = None
        row.side_window_film_code = None
        row.film_code = film_code
        row.area_m2 = payload.area_m2
        row.warranty_expiry = None

    await db.commit()
    row = await _get_warranty_by_serial(db, serial)

    return WarrantyLookupResponse(
        serial=row.serial,
        status=row.status,
        warranty=_make_public_info(row),
    )


@router.get("/admin/warranties", response_model=PaginatedResponse[WarrantyAdminResponse])
async def list_warranties(
    db: Db,
    _: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status_filter: str | None = Query(None, alias="status"),
    search: str | None = Query(None),
):
    query = select(WarrantySerial).options(
        selectinload(WarrantySerial.dealer),
        selectinload(WarrantySerial.film_package),
    )
    count_query = select(func.count(WarrantySerial.id))

    if status_filter:
        query = query.where(WarrantySerial.status == status_filter)
        count_query = count_query.where(WarrantySerial.status == status_filter)

    if search:
        like = f"%{search.strip()}%"
        condition = or_(
            WarrantySerial.serial.ilike(like),
            WarrantySerial.vehicle_plate.ilike(like),
            WarrantySerial.customer_phone.ilike(like),
            WarrantySerial.film_code.ilike(like),
        )
        query = query.where(condition)
        count_query = count_query.where(condition)

    total = (await db.execute(count_query)).scalar() or 0
    rows = (
        await db.execute(
            query.order_by(WarrantySerial.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).scalars().all()

    return PaginatedResponse(
        items=[_serialize_warranty(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=max(1, (total + page_size - 1) // page_size),
    )


@router.patch("/admin/warranties/{warranty_id}", response_model=WarrantyAdminResponse)
async def update_warranty(warranty_id: str, payload: WarrantyAdminUpdate, db: Db, _: CurrentUser):
    row = (
        await db.execute(
            select(WarrantySerial)
            .options(selectinload(WarrantySerial.dealer), selectinload(WarrantySerial.film_package))
            .where(WarrantySerial.id == warranty_id)
        )
    ).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Warranty not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in VALID_SERIAL_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid warranty status")
    if "warranty_type" in update_data and update_data["warranty_type"] not in VALID_WARRANTY_TYPES:
        raise HTTPException(status_code=400, detail="Invalid warranty type")
    if "dealer_id" in update_data:
        dealer_id = update_data["dealer_id"]
        if row.dealer_id and dealer_id != row.dealer_id:
            raise HTTPException(status_code=400, detail="Serial is already assigned to another dealer")
        if dealer_id:
            dealer = (
                await db.execute(
                    select(Dealer).where(
                        Dealer.id == dealer_id,
                        Dealer.status == "active",
                    )
                )
            ).scalar_one_or_none()
            if not dealer:
                raise HTTPException(status_code=400, detail="Invalid dealer")

    for field, value in update_data.items():
        setattr(row, field, value)

    await db.commit()
    row = (
        await db.execute(
            select(WarrantySerial)
            .options(selectinload(WarrantySerial.dealer), selectinload(WarrantySerial.film_package))
            .where(WarrantySerial.id == warranty_id)
        )
    ).scalar_one()
    return _serialize_warranty(row)


@router.post("/admin/warranty-serials/generate", response_model=SerialGenerateResponse)
async def generate_warranty_serials(payload: SerialGenerateRequest, db: Db, _: CurrentUser):
    created: list[WarrantySerial] = []
    base_url = payload.qr_base_url.rstrip("/") if payload.qr_base_url else None
    dealer = (
        await db.execute(
            select(Dealer).where(
                Dealer.id == payload.dealer_id,
                Dealer.status == "active",
            )
        )
    ).scalar_one_or_none()
    if not dealer:
        raise HTTPException(status_code=400, detail="Invalid dealer")

    while len(created) < payload.count:
        serial = _generate_serial(payload.prefix)
        exists = (
            await db.execute(select(WarrantySerial.id).where(WarrantySerial.serial == serial))
        ).scalar_one_or_none()
        if exists:
            continue

        row = WarrantySerial(
            serial=serial,
            qr_url=f"{base_url}/w/{serial}" if base_url else f"/w/{serial}",
            warranty_type=payload.warranty_type,
            dealer_id=dealer.id,
            dealer=dealer,
        )
        db.add(row)
        created.append(row)

    await db.commit()
    serials = [row.serial for row in created]
    rows = (
        await db.execute(
            select(WarrantySerial)
            .options(selectinload(WarrantySerial.dealer), selectinload(WarrantySerial.film_package))
            .where(WarrantySerial.serial.in_(serials))
            .order_by(WarrantySerial.created_at.desc())
        )
    ).scalars().all()

    return SerialGenerateResponse(items=[_serialize_warranty(row) for row in rows])


@router.get("/admin/warranty-serials/export")
async def export_warranty_serials(db: Db, _: CurrentUser):
    rows = (
        await db.execute(
            select(WarrantySerial)
            .options(selectinload(WarrantySerial.dealer), selectinload(WarrantySerial.film_package))
            .order_by(WarrantySerial.created_at.desc())
        )
    ).scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "serial",
        "qr_url",
        "warranty_type",
        "status",
        "vehicle_plate",
        "customer_phone",
        "dealer",
        "film_package",
        "film_code",
        "area_m2",
    ])
    for row in rows:
        writer.writerow([
            row.serial,
            row.qr_url or f"/w/{row.serial}",
            _warranty_type(row),
            row.status,
            row.vehicle_plate or "",
            row.customer_phone or "",
            row.dealer.dealer_name if row.dealer else "",
            row.film_package.package_name if row.film_package else "",
            row.film_code or "",
            row.area_m2 or "",
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=warranty-serials.csv"},
    )


@router.get("/admin/dealers", response_model=list[DealerResponse])
async def list_dealers(db: Db, _: CurrentUser):
    rows = (
        await db.execute(
            select(Dealer, func.count(WarrantySerial.id).label("serial_count"))
            .outerjoin(WarrantySerial, WarrantySerial.dealer_id == Dealer.id)
            .group_by(Dealer.id)
            .order_by(Dealer.dealer_name)
        )
    ).all()

    return [
        DealerResponse.model_validate(dealer).model_copy(update={"serial_count": serial_count})
        for dealer, serial_count in rows
    ]


@router.post("/admin/dealers", response_model=DealerResponse, status_code=201)
async def create_dealer(payload: DealerCreate, db: Db, _: CurrentUser):
    if payload.status not in VALID_ACTIVE_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid dealer status")

    dealer = Dealer(
        dealer_name=payload.dealer_name.strip(),
        activation_code=_normalize_code(payload.activation_code),
        status=payload.status,
    )
    db.add(dealer)
    await db.commit()
    await db.refresh(dealer)
    return dealer


@router.patch("/admin/dealers/{dealer_id}", response_model=DealerResponse)
async def update_dealer(dealer_id: str, payload: DealerUpdate, db: Db, _: CurrentUser):
    dealer = (await db.execute(select(Dealer).where(Dealer.id == dealer_id))).scalar_one_or_none()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in VALID_ACTIVE_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid dealer status")
    if "dealer_name" in update_data and update_data["dealer_name"]:
        update_data["dealer_name"] = update_data["dealer_name"].strip()
    if "activation_code" in update_data and update_data["activation_code"]:
        update_data["activation_code"] = _normalize_code(update_data["activation_code"])

    for field, value in update_data.items():
        setattr(dealer, field, value)

    await db.commit()
    await db.refresh(dealer)
    return dealer


@router.get("/admin/film-packages", response_model=list[FilmPackageResponse])
async def list_film_packages(db: Db, _: CurrentUser):
    return (
        await db.execute(select(FilmPackage).order_by(FilmPackage.warranty_duration_months))
    ).scalars().all()


@router.post("/admin/film-packages", response_model=FilmPackageResponse, status_code=201)
async def create_film_package(payload: FilmPackageCreate, db: Db, _: CurrentUser):
    if payload.status not in VALID_ACTIVE_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid package status")

    package = FilmPackage(
        package_name=payload.package_name.strip(),
        warranty_duration_months=payload.warranty_duration_months,
        status=payload.status,
    )
    db.add(package)
    await db.commit()
    await db.refresh(package)
    return package


@router.patch("/admin/film-packages/{package_id}", response_model=FilmPackageResponse)
async def update_film_package(package_id: str, payload: FilmPackageUpdate, db: Db, _: CurrentUser):
    package = (
        await db.execute(select(FilmPackage).where(FilmPackage.id == package_id))
    ).scalar_one_or_none()
    if not package:
        raise HTTPException(status_code=404, detail="Film package not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in VALID_ACTIVE_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid package status")
    if "package_name" in update_data and update_data["package_name"]:
        update_data["package_name"] = update_data["package_name"].strip()

    for field, value in update_data.items():
        setattr(package, field, value)

    await db.commit()
    await db.refresh(package)
    return package
