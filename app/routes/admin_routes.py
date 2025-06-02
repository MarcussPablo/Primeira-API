from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database, models
from fastapi.security import OAuth2PasswordBearer
from app import auth

router = APIRouter(prefix="/admin", tags=["admin"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    payload = auth.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None or not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

@router.post("/reset_posts", status_code=204)
def reset_posts(db: Session = Depends(database.get_db), admin: models.User = Depends(get_current_admin)):
    db.query(models.Post).delete()
    db.commit()
