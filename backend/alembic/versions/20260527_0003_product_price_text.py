"""Store product prices as display text.

Revision ID: 20260527_0003
Revises: 20260525_0002
Create Date: 2026-05-27
"""

from alembic import op
import sqlalchemy as sa


revision = "20260527_0003"
down_revision = "20260525_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "products",
        "price_sedan",
        existing_type=sa.Integer(),
        type_=sa.String(length=120),
        existing_nullable=True,
        postgresql_using=(
            "CASE WHEN price_sedan IS NULL THEN NULL "
            "ELSE 'Sedan: ' || replace(to_char(price_sedan, 'FM999,999,999,999'), ',', '.') || ' đ' END"
        ),
    )
    op.alter_column(
        "products",
        "price_suv",
        existing_type=sa.Integer(),
        type_=sa.String(length=120),
        existing_nullable=True,
        postgresql_using=(
            "CASE WHEN price_suv IS NULL THEN NULL "
            "ELSE 'SUV: ' || replace(to_char(price_suv, 'FM999,999,999,999'), ',', '.') || ' đ' END"
        ),
    )


def downgrade() -> None:
    op.alter_column(
        "products",
        "price_sedan",
        existing_type=sa.String(length=120),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using="NULLIF(regexp_replace(price_sedan, '\\D', '', 'g'), '')::integer",
    )
    op.alter_column(
        "products",
        "price_suv",
        existing_type=sa.String(length=120),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using="NULLIF(regexp_replace(price_suv, '\\D', '', 'g'), '')::integer",
    )
