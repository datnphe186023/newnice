import logging
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import QuoteRequest, Contact
from app.schemas import (
    QuoteRequestCreate, QuoteRequestResponse,
    ContactCreate, ContactResponse,
    MessageResponse
)
from app.services.email_service import notify_new_quote, notify_new_contact

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Quotes & Contact"])


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
