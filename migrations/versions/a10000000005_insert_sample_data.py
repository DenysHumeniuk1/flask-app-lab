"""Insert sample categories and products manually.

Revision ID: a10000000005
Revises: a10000000004
"""
from alembic import op
import sqlalchemy as sa

revision = "a10000000005"
down_revision = "a10000000004"
branch_labels = None
depends_on = None


def upgrade():
    categories = sa.table(
        "categories",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )
    products = sa.table(
        "products",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("price", sa.Float),
        sa.column("active", sa.Boolean),
        sa.column("category_id", sa.Integer),
    )

    op.bulk_insert(categories, [
        {"id": 1, "name": "Electronics"},
        {"id": 2, "name": "Books"},
        {"id": 3, "name": "Clothing"},
    ])
    op.bulk_insert(products, [
        {"id": 1, "name": "Laptop", "price": 1200.0, "active": True, "category_id": 1},
        {"id": 2, "name": "Smartphone", "price": 800.0, "active": True, "category_id": 1},
        {"id": 3, "name": "Novel", "price": 20.0, "active": True, "category_id": 2},
        {"id": 4, "name": "T-Shirt", "price": 25.0, "active": False, "category_id": 3},
    ])


def downgrade():
    op.execute("DELETE FROM products WHERE id IN (1, 2, 3, 4)")
    op.execute("DELETE FROM categories WHERE id IN (1, 2, 3)")
