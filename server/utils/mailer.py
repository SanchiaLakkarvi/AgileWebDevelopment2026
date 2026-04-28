from flask import current_app, url_for
from flask_mail import Message

from server.extensions import mail


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
