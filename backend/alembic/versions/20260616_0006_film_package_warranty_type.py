"""scope warranty packages by warranty type

Revision ID: 20260616_0006
Revises: 20260616_0005
Create Date: 2026-06-16 00:00:00.000000
"""

from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


revision: str = "20260616_0006"
down_revision: Union[str, None] = "20260616_0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "film_packages",
        sa.Column("warranty_type", sa.String(length=30), nullable=False, server_default="auto_film"),
    )
    op.drop_index("ix_film_packages_package_name", table_name="film_packages")
    op.create_index("ix_film_packages_package_name", "film_packages", ["package_name"], unique=False)
    op.create_index("ix_film_packages_warranty_type", "film_packages", ["warranty_type"], unique=False)
    op.create_unique_constraint(
        "uq_film_packages_type_name",
        "film_packages",
        ["warranty_type", "package_name"],
    )

    now = datetime.utcnow()
    package_table = sa.table(
        "film_packages",
        sa.column("id", sa.String),
        sa.column("package_name", sa.String),
        sa.column("warranty_type", sa.String),
        sa.column("warranty_duration_months", sa.Integer),
        sa.column("status", sa.String),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
    )
    op.bulk_insert(
        package_table,
        [
            {
                "id": str(uuid4()),
                "package_name": "Standard",
                "warranty_type": "auto_ppf",
                "warranty_duration_months": 36,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "Plus",
                "warranty_type": "auto_ppf",
                "warranty_duration_months": 60,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "Premium",
                "warranty_type": "auto_ppf",
                "warranty_duration_months": 84,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "Flagship",
                "warranty_type": "auto_ppf",
                "warranty_duration_months": 120,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "NewNice Eco",
                "warranty_type": "building_film",
                "warranty_duration_months": 12,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "NewNice Basic",
                "warranty_type": "building_film",
                "warranty_duration_months": 24,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "NewNice Pro",
                "warranty_type": "building_film",
                "warranty_duration_months": 60,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "NewNice Luxury",
                "warranty_type": "building_film",
                "warranty_duration_months": 96,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "Film bảo vệ",
                "warranty_type": "kitchen_ppf",
                "warranty_duration_months": 12,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "Film PPF",
                "warranty_type": "kitchen_ppf",
                "warranty_duration_months": 48,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "NewNice Pro",
                "warranty_type": "kitchen_ppf",
                "warranty_duration_months": 96,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": str(uuid4()),
                "package_name": "NewNice Luxury",
                "warranty_type": "kitchen_ppf",
                "warranty_duration_months": 120,
                "status": "active",
                "created_at": now,
                "updated_at": now,
            },
        ],
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM film_packages
        WHERE (warranty_type = 'auto_ppf' AND package_name IN ('Standard', 'Plus', 'Premium', 'Flagship'))
           OR (warranty_type = 'building_film' AND package_name IN ('NewNice Eco', 'NewNice Basic', 'NewNice Pro', 'NewNice Luxury'))
           OR (warranty_type = 'kitchen_ppf' AND package_name IN ('Film bảo vệ', 'Film PPF', 'NewNice Pro', 'NewNice Luxury'))
        """
    )
    op.drop_constraint("uq_film_packages_type_name", "film_packages", type_="unique")
    op.drop_index("ix_film_packages_warranty_type", table_name="film_packages")
    op.drop_index("ix_film_packages_package_name", table_name="film_packages")
    op.create_index("ix_film_packages_package_name", "film_packages", ["package_name"], unique=True)
    op.drop_column("film_packages", "warranty_type")
