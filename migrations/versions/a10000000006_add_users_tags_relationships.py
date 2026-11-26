"""Add users, tags and Post relationships; migrate legacy author names.

Revision ID: a10000000006
Revises: a10000000005
"""
from alembic import op
import sqlalchemy as sa
import re

revision = "a10000000006"
down_revision = "a10000000005"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("username", name="uq_users_username"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_tags"),
        sa.UniqueConstraint("name", name="uq_tags_name"),
    )

    bind = op.get_bind()
    legacy_authors = bind.execute(sa.text(
        "SELECT DISTINCT author FROM posts ORDER BY author"
    )).scalars().all()
    if not legacy_authors:
        legacy_authors = ["Anonymous"]

    author_ids = {}
    used_usernames = set()
    for index, author in enumerate(legacy_authors, start=1):
        original = (author or "Anonymous").strip() or "Anonymous"
        base = re.sub(r"[^a-zA-Z0-9_-]+", "_", original).strip("_").lower() or "user"
        username = base[:65]
        suffix = 1
        while username in used_usernames:
            suffix += 1
            username = f"{base[:65]}_{suffix}"
        used_usernames.add(username)
        email = f"{username}_{index}@example.com"
        bind.execute(sa.text(
            "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)"
        ), {"username": username, "email": email, "password": "change-me"})
        new_id = bind.execute(sa.text("SELECT id FROM users WHERE username = :username"),
                              {"username": username}).scalar_one()
        author_ids[author] = new_id

    with op.batch_alter_table("posts") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))

    for old_author, user_id in author_ids.items():
        bind.execute(sa.text("UPDATE posts SET user_id = :user_id WHERE author = :author"),
                     {"user_id": user_id, "author": old_author})

    with op.batch_alter_table("posts") as batch_op:
        batch_op.alter_column("user_id", existing_type=sa.Integer(), nullable=False)
        batch_op.create_foreign_key(
            "fk_posts_user_id_users", "users", ["user_id"], ["id"]
        )
        batch_op.drop_column("author")

    op.create_table(
        "post_tags",
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], name="fk_post_tags_post_id_posts", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"], name="fk_post_tags_tag_id_tags", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("post_id", "tag_id", name="pk_post_tags"),
    )


def downgrade():
    op.drop_table("post_tags")
    with op.batch_alter_table("posts") as batch_op:
        batch_op.add_column(sa.Column("author", sa.String(length=20), nullable=True))
        batch_op.drop_constraint("fk_posts_user_id_users", type_="foreignkey")
        batch_op.drop_column("user_id")
    op.execute("UPDATE posts SET author = 'Anonymous' WHERE author IS NULL")
    op.drop_table("tags")
    op.drop_table("users")
