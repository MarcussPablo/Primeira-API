from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, database, auth
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime

router = APIRouter(prefix="/posts", tags=["posts"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    payload = auth.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    username = payload.get("sub")
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    # Check if visitor expired
    if user.is_visitor and user.expire_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Visitor account expired")
    return user

@router.get("/", response_model=List[schemas.PostOut])
def list_posts(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts

@router.post("/", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    new_post = models.Post(title=post.title, content=post.content, owner_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    db.delete(db_post)
    db.commit()
