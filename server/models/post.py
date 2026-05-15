from datetime import datetime

from server.extensions import db


class ForumPost(db.Model):
    __tablename__ = "forum_posts"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(30), nullable=False, default="Study")

    author = db.Column(db.String(80), nullable=False)
    author_email = db.Column(db.String(120), nullable=True)

    image_url = db.Column(db.String(255), nullable=True)

    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("register_data.id"), nullable=True)

    comments = db.relationship(
        "ForumComment",
        backref="post",
        lazy=True,
        cascade="all, delete-orphan"
    )


class ForumComment(db.Model):
    __tablename__ = "forum_comments"

    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String(240), nullable=False)
    author = db.Column(db.String(80), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    post_id = db.Column(db.Integer, db.ForeignKey("forum_posts.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("register_data.id"), nullable=True)