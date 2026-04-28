import os
from datetime import datetime

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_mail import Message

from server.extensions import db, mail
from server.forum.models import Comment, Post

forum_bp = Blueprint("forum", __name__)
ALLOWED_CATEGORIES = {"Study", "Events", "Life", "LostFound"}
ALLOWED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def category_label(category: str) -> str:
    return "Lost & Found" if category == "LostFound" else category


def format_dt(value) -> str:
    if not value:
        return ""
    return value.strftime("%Y-%m-%d %H:%M")


def relative_time(value) -> str:
    if not value:
        return "just now"

    now = datetime.utcnow()
    diff = now - value
    total_seconds = int(diff.total_seconds())

    if total_seconds < 60:
        return "just now"
    if total_seconds < 3600:
        return f"{total_seconds // 60}m ago"
    if total_seconds < 86400:
        return f"{total_seconds // 3600}h ago"
    if total_seconds < 7 * 86400:
        return f"{total_seconds // 86400}d ago"
    return format_dt(value)


def send_comment_notification(post, comment_author: str, comment_text: str) -> bool:
    """Send email notification to post owner when a new comment is added."""

    recipient = (post.author_email or "").strip()
    if not recipient:
        return False

    if not current_app.config.get("MAIL_SERVER"):
        return False

    msg = Message(
        subject=f"GuildSpace: new comment on '{post.title}'",
        recipients=[recipient],
    )
    msg.body = (
        f"Hi {post.author},\n\n"
        f"You have a new comment on your post '{post.title}'.\n\n"
        f"Comment by: {comment_author}\n"
        f"Comment: {comment_text}\n\n"
        f"Open forum: {url_for('forum.forum_page', _external=True)}\n"
    )
    mail.send(msg)
    return True


@forum_bp.app_context_processor
def inject_template_helpers():
    # Expose formatting helpers directly to Jinja templates.
    return {
        "category_label": category_label,
        "format_dt": format_dt,
        "relative_time": relative_time,
    }


@forum_bp.get("/forum")
def forum_page() -> str:
    posts = db.session.scalars(db.select(Post).order_by(Post.created_at.desc())).all()
    return render_template(
        "forum.html",
        page_title="GuildSpace | Forum",
        active_nav="forum",
        posts=posts,
    )


@forum_bp.post("/forum/post")
def create_post():
    author = str(request.form.get("author", "")).strip()
    author_email = str(request.form.get("author_email", "")).strip()
    title = str(request.form.get("title", "")).strip()
    content = str(request.form.get("content", "")).strip()
    category = str(request.form.get("category", "")).strip()
    image_url = ""

    if not author or not title or not content or category not in ALLOWED_CATEGORIES:
        flash("Please fill all required fields.", "danger")
        return redirect(url_for("forum.forum_page"))

    image_file = request.files.get("image_file")
    if image_file and image_file.filename:
        uploads_dir = os.path.join("src", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)

        ext = os.path.splitext(image_file.filename)[1].lower()
        if ext not in ALLOWED_IMAGE_EXTS:
            flash("Please upload png/jpg/jpeg/webp/gif image.", "danger")
            return redirect(url_for("forum.forum_page"))

        filename = f"{int(datetime.utcnow().timestamp() * 1000)}{ext}"
        save_path = os.path.join(uploads_dir, filename)

        try:
            image_file.save(save_path)
            image_url = url_for("static", filename=f"uploads/{filename}")
        except OSError:
            flash("Image upload failed. Please try again.", "danger")
            return redirect(url_for("forum.forum_page"))

    post = Post(
        author=author,
        author_email=author_email,
        title=title,
        content=content,
        category=category,
        image_url=image_url,
    )
    db.session.add(post)
    db.session.commit()

    flash("Post published.", "success")
    return redirect(url_for("forum.forum_page", _anchor=f"post-{post.id}"))


@forum_bp.post("/forum/<int:post_id>/like")
def like_post(post_id: int):
    post = db.get_or_404(Post, post_id)
    post.likes = int(post.likes or 0) + 1
    db.session.commit()
    return redirect(url_for("forum.forum_page", _anchor=f"post-{post_id}"))


@forum_bp.post("/forum/<int:post_id>/dislike")
def dislike_post(post_id: int):
    post = db.get_or_404(Post, post_id)
    post.dislikes = int(post.dislikes or 0) + 1
    db.session.commit()
    return redirect(url_for("forum.forum_page", _anchor=f"post-{post_id}"))


@forum_bp.post("/forum/<int:post_id>/comment")
def add_comment(post_id: int):
    post = db.get_or_404(Post, post_id)

    author = str(request.form.get("author", "You")).strip() or "You"
    text = str(request.form.get("text", "")).strip()
    if not text:
        flash("Comment cannot be empty.", "danger")
        return redirect(url_for("forum.forum_page", _anchor=f"post-{post_id}"))

    db.session.add(
        Comment(
            post_id=post_id,
            author=author,
            text=text,
        )
    )
    db.session.commit()

    try:
        sent = send_comment_notification(post, author, text)
        if sent:
            flash("Comment added. Email notification sent.", "success")
            return redirect(url_for("forum.forum_page", _anchor=f"post-{post_id}"))
    except Exception:
        flash("Comment added, but email notification failed.", "warning")
        return redirect(url_for("forum.forum_page", _anchor=f"post-{post_id}"))

    # PRG pattern: avoid duplicate form submissions on refresh.
    flash("Comment added.", "success")
    return redirect(url_for("forum.forum_page", _anchor=f"post-{post_id}"))
