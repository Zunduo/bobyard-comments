from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import crud
from app.db import Base, SessionLocal, engine, get_db
from app.schemas import CommentCreate, CommentOut, CommentUpdate
from app.seed import seed_if_empty


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Bobyard Comments API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/comments", response_model=list[CommentOut])
def list_comments(db: Session = Depends(get_db)):
    return crud.list_comments(db)


@app.post("/api/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def add_comment(payload: CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db, payload)

 
@app.patch("/api/comments/{comment_id}", response_model=CommentOut)
def edit_comment(comment_id: str, payload: CommentUpdate, db: Session = Depends(get_db)):
    comment = crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    return crud.update_comment(db, comment, payload)


@app.delete("/api/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_comment(comment_id: str, db: Session = Depends(get_db)):
    comment = crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    crud.delete_comment(db, comment)
    return None
