"""Initial migration

Revision ID: 9f244bd6ca90
Revises: 
Create Date: 2026-11-12 11:29:13.533678

"""
from alembic import op
import sqlalchemy as sa


revision = '9f244bd6ca90'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('posted', sa.DateTime(), nullable=False),
    sa.Column('category', sa.Enum('news', 'publication', 'tech', 'other', name='post_category'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('posts')
