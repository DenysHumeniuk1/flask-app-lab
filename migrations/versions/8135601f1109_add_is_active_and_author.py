"""add is_active and author

Revision ID: 8135601f1109
Revises: 9f244bd6ca90
Create Date: 2026-11-12 11:31:41.332170

"""
from alembic import op
import sqlalchemy as sa


revision = '8135601f1109'
down_revision = '9f244bd6ca90'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('author', sa.String(length=20), nullable=False))


def downgrade():
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('author')
        batch_op.drop_column('is_active')
