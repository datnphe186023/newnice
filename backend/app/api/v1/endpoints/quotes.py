from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import QuoteRequest, Contact
from app.schemas import (
    QuoteRequestCreate, QuoteRequestResponse,
    ContactCreate, ContactResponse,
    MessageResponse
)

router = APIRouter(tags=["Quotes & Contact"])


@router.post("/quotes", response_model=QuoteRequestResponse)
async def create_quote_request(
    data: QuoteRequestCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Submit a quote request"""
    quote = QuoteRequest(**data.model_dump())
    db.add(quote)
    await db.commit()
    await db.refresh(quote)
    return quote


@router.post("/contact", response_model=MessageResponse)
async def create_contact(
    data: ContactCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Submit a contact message"""
    contact = Contact(**data.model_dump())
    db.add(contact)
    await db.commit()
    
    return MessageResponse(
        message="Cảm ơn bạn đã liên hệ. Chúng tôi sẽ phản hồi trong thời gian sớm nhất!",
        success=True
    )
