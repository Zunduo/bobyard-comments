from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Comment
from app.schemas import CommentCreate, CommentUpdate


def list_comments(db: Session) -> list[Comment]:
    return list(db.scalars(select(Comment).order_by(Comment.date.asc(), Comment.id.asc())))


def get_comment(db: Session, comment_id: str) -> Comment | None:
    return db.get(Comment, comment_id)


def create_comment(db: Session, payload: CommentCreate) -> Comment:
    comment = Comment(
        id=str(uuid.uuid4()),
        author="Admin",
        text=payload.text.strip(),
        date=datetime.now(timezone.utc),
        likes=0,
        image="",
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def update_comment(db: Session, comment: Comment, payload: CommentUpdate) -> Comment:
    comment.text = payload.text.strip()
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: Session, comment: Comment) -> None:
    db.delete(comment)
    db.commit()
