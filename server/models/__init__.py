from server.models.post import ForumPost, ForumComment

# Backward-compatible aliases in case older route files still import Post/Comment.
Post = ForumPost
Comment = ForumComment

__all__ = ["ForumPost", "ForumComment", "Post", "Comment"]
