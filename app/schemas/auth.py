from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token:str
    token_type: str

class tokenData(BaseModel):
    email: str | None = None

class ChangePassword(BaseModel):
    old_password: str
    new_password: str