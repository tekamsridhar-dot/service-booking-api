from urllib import request

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.schemas.user import UserCreate,UserResponse
from app.schemas.auth import Token,ChangePassword
from app.schemas.user import UserResponse,UserCreate
from app.repository import user_repository
from app.core.security import verify_password, create_access_token,hash_password

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse)
def register(request:UserCreate,db:Session=Depends(get_db)):
    existing_user=user_repository.get_user_by_email(db,request.email)
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")

    user=User(full_name=request.full_name,email=request.email,phone=request.phone,
              hashed_password=hash_password(request.password),role=request.role)
    return user_repository.create_user(db,user)

@router.post("/login",response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user=user_repository.get_user_by_email(db,form_data.username)
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid email or password")
    access_token=create_access_token(data={"sub":user.email})
    return {"access_token":access_token,"token_type":"bearer"}

@router.get("/profile",response_model=UserResponse)
def get_profile(current_user:User=Depends(get_current_user)):
    return current_user

@router.post("/change-password")
def change_password(request:ChangePassword,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if not verify_password(request.old_password,current_user.hashed_password):
        raise HTTPException(status_code=400,detail="Old password is incorrect")
    current_user.hashed_password=hash_password(request.new_password)
    db.commit()
    return {"message":"Password changed successfully"}