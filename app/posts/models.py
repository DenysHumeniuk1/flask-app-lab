from datetime import datetime
from ..extensions import db

post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    posts = db.relationship(
        "Post", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username!r})>"


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    posts = db.relationship("Post", secondary=post_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name!r})>"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(
        db.Enum("news", "publication", "tech", "other", name="post_category"),
        nullable=False,
        default="other",
    )
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="posts")
    tags = db.relationship("Tag", secondary=post_tags, back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title!r})>"
