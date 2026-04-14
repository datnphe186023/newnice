"""
Admin site settings CRUD.
Settings are stored as key-value pairs (key, value, setting_type).
All routes require authenticated admin user.
"""
import json
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import AdminUser
from app.models.content import SiteSetting
from app.api.deps import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/settings", tags=["Admin - Settings"])

Db = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[AdminUser, Depends(get_current_user)]


class SettingOut(BaseModel):
    key: str
    value: str | None
    setting_type: str

    class Config:
        from_attributes = True


class SettingsBulkUpdate(BaseModel):
    """Map of key → value for bulk upsert."""
    settings: dict[str, str | None]


# ---------------------------------------------------------------------------
# Default settings definition (used to seed missing keys)
# ---------------------------------------------------------------------------

DEFAULT_SETTINGS: dict[str, tuple[str, str]] = {
    # key: (default_value, setting_type)
    "site_name":          ("Newnice", "text"),
    "site_tagline":       ("Phim cách nhiệt ô tô cao cấp", "text"),
    "contact_phone":      ("0869 418 104", "text"),
    "contact_email":      ("newnicefilm@gmail.com", "text"),
    "contact_address":    ("311 Phúc Diễn, Nam Từ Liêm, Hà Nội", "text"),
    "facebook_url":       ("https://facebook.com/newnicevn", "text"),
    "zalo_url":           ("https://zalo.me/0869418104", "text"),
    "youtube_url":        ("", "text"),
    "footer_about":       ("Chuyên cung cấp và thi công phim cách nhiệt ô tô, phim đổi màu xe, phim cách nhiệt nhà kính cao cấp.", "text"),
    "hero_phone":         ("0869 418 104", "text"),
    "ga_measurement_id":  ("", "text"),
    "gsc_verification":   ("", "text"),
    "warranty_headline":  ("Bảo hành lên đến 10 năm", "text"),
    "meta_description":   ("Newnice - Chuyên cung cấp và thi công phim cách nhiệt ô tô, phim đổi màu xe, phim nhà kính cao cấp tại Hà Nội", "text"),
}


async def _seed_defaults(db: AsyncSession) -> None:
    """Insert missing default settings rows."""
    existing = set(
        row.key for row in (await db.execute(select(SiteSetting.key))).scalars().all()
    )
    for key, (value, stype) in DEFAULT_SETTINGS.items():
        if key not in existing:
            db.add(SiteSetting(key=key, value=value, setting_type=stype))
    await db.commit()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("", response_model=list[SettingOut])
async def get_settings(db: Db, _: CurrentUser):
    """Return all site settings, seeding defaults for any missing keys."""
    await _seed_defaults(db)
    rows = (await db.execute(select(SiteSetting).order_by(SiteSetting.key))).scalars().all()
    return rows


@router.patch("", response_model=list[SettingOut])
async def update_settings(payload: SettingsBulkUpdate, db: Db, current_user: CurrentUser):
    """Bulk upsert settings. Accepts a dict of {key: value}."""
    for key, value in payload.settings.items():
        row = (await db.execute(select(SiteSetting).where(SiteSetting.key == key))).scalar_one_or_none()
        if row:
            row.value = value
        else:
            stype = DEFAULT_SETTINGS.get(key, ("", "text"))[1]
            db.add(SiteSetting(key=key, value=value, setting_type=stype))

    await db.commit()
    rows = (await db.execute(select(SiteSetting).order_by(SiteSetting.key))).scalars().all()
    logger.info("Site settings updated by %s", current_user.email)
    return rows
