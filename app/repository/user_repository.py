from sqlalchemy.orm import Session
from app.models import User
from datetime import datetime,timedelta
from jose import jwt
from app.core.config import SECRET_KEY,ALGORITHM

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user: User):
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User):
    user.is_deleted = True
    db.commit()

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=7)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)