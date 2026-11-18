"""Add active flag to products.

Revision ID: a10000000003
Revises: a10000000002
"""
from alembic import op
import sqlalchemy as sa

revision = "a10000000003"
down_revision = "a10000000002"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("products") as batch_op:
        batch_op.add_column(sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()))


def downgrade():
    with op.batch_alter_table("products") as batch_op:
        batch_op.drop_column("active")
