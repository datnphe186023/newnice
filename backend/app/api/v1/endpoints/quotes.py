import logging
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import QuoteRequest, Contact, AdminUser
from app.schemas import (
    QuoteRequestCreate, QuoteRequestResponse,
    ContactCreate, ContactResponse, QuoteRequestUpdate,
    PaginatedResponse,
    MessageResponse
)
from app.api.deps import get_current_user
from app.services.email_service import notify_new_quote, notify_new_contact

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Quotes & Contact"])


@router.get("/quotes", response_model=PaginatedResponse[QuoteRequestResponse])
async def get_quotes(
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AdminUser, Depends(get_current_user)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: str | None = Query(None),
    search: str | None = Query(None),
):
    query = select(QuoteRequest)
    count_query = select(func.count(QuoteRequest.id))

    if status:
        query = query.where(QuoteRequest.status == status)
        count_query = count_query.where(QuoteRequest.status == status)

    if search:
        like = f"%{search}%"
        condition = or_(QuoteRequest.customer_name.ilike(like), QuoteRequest.phone.ilike(like))
        query = query.where(condition)
        count_query = count_query.where(condition)

    total = (await db.execute(count_query)).scalar() or 0
    items = (
        await db.execute(
            query
            .order_by(QuoteRequest.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).scalars().all()

    total_pages = max(1, (total + page_size - 1) // page_size)
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.put("/quotes/{quote_id}", response_model=QuoteRequestResponse)
async def update_quote(
    quote_id: int,
    data: QuoteRequestUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AdminUser, Depends(get_current_user)],
):
    quote = (await db.execute(select(QuoteRequest).where(QuoteRequest.id == quote_id))).scalar_one_or_none()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(quote, field, value)

    await db.commit()
    await db.refresh(quote)
    return quote


@router.get("/contacts", response_model=PaginatedResponse[ContactResponse])
async def get_contacts(
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AdminUser, Depends(get_current_user)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    count_query = select(func.count(Contact.id))
    total = (await db.execute(count_query)).scalar() or 0
    items = (
        await db.execute(
            select(Contact)
            .order_by(Contact.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).scalars().all()

    total_pages = max(1, (total + page_size - 1) // page_size)
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.put("/contacts/{contact_id}/read", response_model=ContactResponse)
async def mark_contact_as_read(
    contact_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AdminUser, Depends(get_current_user)],
):
    contact = (await db.execute(select(Contact).where(Contact.id == contact_id))).scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    contact.is_read = True
    await db.commit()
    await db.refresh(contact)
    return contact


@router.post("/quotes", response_model=QuoteRequestResponse, status_code=201)
async def create_quote_request(
    data: QuoteRequestCreate,
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Submit a quote request.

    Saves the request to the database and fires email notifications
    (admin alert + optional customer confirmation) in the background —
    so the response is immediate regardless of SMTP latency.
    """
    quote = QuoteRequest(**data.model_dump())
    db.add(quote)
    await db.commit()
    await db.refresh(quote)

    # Fire-and-forget email — runs after response is sent
    background_tasks.add_task(
        notify_new_quote,
        customer_name=data.customer_name,
        phone=data.phone,
        email=data.email,
        car_brand=data.car_brand,
        car_model=data.car_model,
        car_year=data.car_year,
        service_type=data.service_type,
        film_type_preference=data.film_type_preference,
        message=data.message,
    )

    return quote


@router.post("/contact", response_model=MessageResponse, status_code=201)
async def create_contact(
    data: ContactCreate,
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Submit a contact message.

    Saves to DB and fires email notifications in the background.
    Always returns success immediately — email failures are logged but
    do not affect the API response.
    """
    contact = Contact(**data.model_dump())
    db.add(contact)
    await db.commit()

    background_tasks.add_task(
        notify_new_contact,
        name=data.name,
        email=data.email,
        phone=data.phone,
        subject=data.subject,
        message=data.message,
    )

    return MessageResponse(
        message="Cảm ơn bạn đã liên hệ. Chúng tôi sẽ phản hồi trong thời gian sớm nhất!",
        success=True,
    )
