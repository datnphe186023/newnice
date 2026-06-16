"""support multiple warranty types

Revision ID: 20260616_0005
Revises: 20260614_0004
Create Date: 2026-06-16 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260616_0005"
down_revision: Union[str, None] = "20260614_0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "warranty_serials",
        sa.Column("warranty_type", sa.String(length=30), nullable=False, server_default="auto_film"),
    )
    op.add_column("warranty_serials", sa.Column("film_code", sa.String(length=100), nullable=True))
    op.add_column("warranty_serials", sa.Column("area_m2", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("warranty_serials", "area_m2")
    op.drop_column("warranty_serials", "film_code")
    op.drop_column("warranty_serials", "warranty_type")
