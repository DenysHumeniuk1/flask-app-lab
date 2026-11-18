"""Create products table for ORM migration lab.

Revision ID: a10000000001
Revises: 8135601f1109
"""
from alembic import op
import sqlalchemy as sa

revision = "a10000000001"
down_revision = "8135601f1109"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_products"),
    )


def downgrade():
    op.drop_table("products")
