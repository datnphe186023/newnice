"""warranty module

Revision ID: 20260525_0002
Revises: 20260424_0001
Create Date: 2026-05-25 00:00:00.000000
"""

from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


revision: str = "20260525_0002"
down_revision: Union[str, None] = "20260424_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dealers",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("dealer_name", sa.String(length=255), nullable=False),
        sa.Column("activation_code", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_dealers_activation_code", "dealers", ["activation_code"], unique=True)

    op.create_table(
        "film_packages",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("package_name", sa.String(length=255), nullable=False),
        sa.Column("warranty_duration_months", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_film_packages_package_name", "film_packages", ["package_name"], unique=True)

    op.create_table(
        "warranty_serials",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("serial", sa.String(length=50), nullable=False),
        sa.Column("qr_url", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="unused"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("activated_at", sa.DateTime(), nullable=True),
        sa.Column("dealer_id", sa.String(length=36), sa.ForeignKey("dealers.id"), nullable=True),
        sa.Column("customer_name", sa.String(length=255), nullable=True),
        sa.Column("customer_phone", sa.String(length=20), nullable=True),
        sa.Column("vehicle_plate", sa.String(length=30), nullable=True),
        sa.Column("vehicle_model", sa.String(length=255), nullable=True),
        sa.Column("film_package_id", sa.String(length=36), sa.ForeignKey("film_packages.id"), nullable=True),
        sa.Column("front_windshield_film_code", sa.String(length=100), nullable=True),
        sa.Column("rear_windshield_film_code", sa.String(length=100), nullable=True),
        sa.Column("side_window_film_code", sa.String(length=100), nullable=True),
        sa.Column("install_date", sa.Date(), nullable=True),
        sa.Column("warranty_expiry", sa.Date(), nullable=True),
    )
    op.create_index("ix_warranty_serials_serial", "warranty_serials", ["serial"], unique=True)
    op.create_index("ix_warranty_serials_status", "warranty_serials", ["status"])

    now = datetime.utcnow()
    op.bulk_insert(
        sa.table(
            "film_packages",
            sa.column("id", sa.String),
            sa.column("package_name", sa.String),
            sa.column("warranty_duration_months", sa.Integer),
            sa.column("status", sa.String),
            sa.column("created_at", sa.DateTime),
            sa.column("updated_at", sa.DateTime),
        ),
        [
            {
                "id": str(uuid4()),
                "package_name": "Standard",
                "warranty_duration_months": 36,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "Plus",
                "warranty_duration_months": 60,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "Premium",
                "warranty_duration_months": 84,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "Flagship",
                "warranty_duration_months": 120,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_warranty_serials_status", table_name="warranty_serials")
    op.drop_index("ix_warranty_serials_serial", table_name="warranty_serials")
    op.drop_table("warranty_serials")
    op.drop_index("ix_film_packages_package_name", table_name="film_packages")
    op.drop_table("film_packages")
    op.drop_index("ix_dealers_activation_code", table_name="dealers")
    op.drop_table("dealers")
