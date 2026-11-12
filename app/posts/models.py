from datetime import datetime
from ..extensions import db

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(
        db.Enum("news", "publication", "tech", "other", name="post_category"),
        nullable=False, default="other"
    )
    
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    author = db.Column(db.String(20), nullable=False, default="Anonymous")

    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title!r})>"
