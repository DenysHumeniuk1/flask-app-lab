"""Add created_at timestamp to products.

Revision ID: a10000000004
Revises: a10000000003
"""
from alembic import op
import sqlalchemy as sa

revision = "a10000000004"
down_revision = "a10000000003"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("products") as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            )
        )


def downgrade():
    with op.batch_alter_table("products") as batch_op:
        batch_op.drop_column("created_at")
