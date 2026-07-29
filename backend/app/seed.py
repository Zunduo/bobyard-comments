from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Comment

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "comments.json"


def _parse_date(value: str) -> datetime:
    # JSON uses "...Z"; fromisoformat wants "+00:00"
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def seed_if_empty(db: Session) -> None:
    count = db.scalar(select(func.count()).select_from(Comment)) or 0
    if count > 0:
        return

    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for item in raw.get("comments", []):
        db.add(
            Comment(
                id=str(item["id"]),
                author=item["author"],
                text=item["text"],
                date=_parse_date(item["date"]),
                likes=int(item.get("likes", 0)),
                image=item.get("image") or "",
            )
        )
    db.commit()
