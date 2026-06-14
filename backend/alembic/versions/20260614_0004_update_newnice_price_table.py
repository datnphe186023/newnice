"""Update Newnice automotive film price table.

Revision ID: 20260614_0004
Revises: 20260527_0003
Create Date: 2026-06-14
"""

from typing import Sequence, Union

from alembic import op


revision: str = "20260614_0004"
down_revision: Union[str, None] = "20260527_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE categories
        SET description = 'Các dòng phim cách nhiệt ô tô Newnice - Eco, Plus, Pro, Royal.'
        WHERE slug = 'phim-cach-nhiet-newnice'
        """
    )
    op.execute(
        """
        UPDATE products
        SET price_sedan = 'Sedan: 5.500.000 đ',
            price_suv = 'SUV: 6.700.000 đ',
            updated_at = CURRENT_TIMESTAMP
        WHERE slug = 'newnice-eco'
        """
    )
    op.execute(
        """
        UPDATE products
        SET name = 'Newnice Plus',
            slug = 'newnice-plus',
            film_code = 'PLUS',
            short_description = 'Gói phim cách nhiệt Newnice Plus - cân bằng giữa hiệu quả cách nhiệt và chi phí.',
            price_sedan = 'Sedan: 7.500.000 đ',
            price_suv = 'SUV: 8.700.000 đ',
            updated_at = CURRENT_TIMESTAMP
        WHERE slug = 'newnice-premium'
        """
    )
    op.execute(
        """
        UPDATE products
        SET name = 'Newnice Pro',
            slug = 'newnice-pro',
            film_code = 'PRO',
            short_description = 'Gói phim cách nhiệt Newnice Pro - hiệu quả cách nhiệt cao cho nhu cầu sử dụng chuyên sâu.',
            price_sedan = 'Sedan: 11.500.000 đ',
            price_suv = 'SUV: 12.900.000 đ',
            updated_at = CURRENT_TIMESTAMP
        WHERE slug = 'newnice-crystal'
        """
    )
    op.execute(
        """
        UPDATE products
        SET price_sedan = 'Sedan: 14.000.000 đ',
            price_suv = 'SUV: 15.500.000 đ',
            updated_at = CURRENT_TIMESTAMP
        WHERE slug = 'newnice-royal'
        """
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE categories
        SET description = 'Các dòng phim cách nhiệt ô tô Newnice - Eco, Premium, Crystal, Royal.'
        WHERE slug = 'phim-cach-nhiet-newnice'
        """
    )
    op.execute(
        """
        UPDATE products
        SET price_sedan = 'Sedan: 5.800.000 đ',
            price_suv = 'SUV: 7.000.000 đ',
            updated_at = CURRENT_TIMESTAMP
        WHERE slug = 'newnice-eco'
        """
    )
    op.execute(
        """
        UPDATE products
        SET name = 'Newnice Premium',
            slug = 'newnice-premium',
            film_code = 'NP',
            short_description = 'Gói phim cách nhiệt Newnice Premium - cân bằng giữa giá và chất lượng.',
            price_sedan = 'Sedan: 10.500.000 đ',
            price_suv = 'SUV: 11.500.000 đ',
            updated_at = CURRENT_TIMESTAMP
        WHERE slug = 'newnice-plus'
        """
    )
    op.execute(
        """
        UPDATE products
        SET name = 'Newnice Crystal',
            slug = 'newnice-crystal',
            film_code = 'NC',
            short_description = 'Gói phim cách nhiệt Newnice Crystal - độ trong cao, cách nhiệt vượt trội.',
            price_sedan = 'Sedan: 12.500.000 đ',
            price_suv = 'SUV: 14.500.000 đ',
            updated_at = CURRENT_TIMESTAMP
        WHERE slug = 'newnice-pro'
        """
    )
    op.execute(
        """
        UPDATE products
        SET price_sedan = 'Sedan: 15.500.000 đ',
            price_suv = 'SUV: 17.500.000 đ',
            updated_at = CURRENT_TIMESTAMP
        WHERE slug = 'newnice-royal'
        """
    )
