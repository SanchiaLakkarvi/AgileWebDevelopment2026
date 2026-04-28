from datetime import datetime

from server.extensions import db


class Post(db.Model):
    """Forum post entity."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(40), nullable=False)
    author_email = db.Column(db.String(120), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String(500), nullable=False, default="")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)

    comments = db.relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
        order_by="Comment.created_at.asc()",
        lazy=True,
    )


class Comment(db.Model):
    """Comment entity linked to a post."""

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    author = db.Column(db.String(40), nullable=False)
    text = db.Column(db.String(240), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    post = db.relationship("Post", back_populates="comments")
