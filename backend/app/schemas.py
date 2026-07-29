from datetime import datetime

from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    text: str = Field(min_length=1)


class CommentUpdate(BaseModel):
    text: str = Field(min_length=1)


class CommentOut(BaseModel):
    id: str
    author: str
    text: str
    date: datetime
    likes: int
    image: str

    model_config = {"from_attributes": True}
