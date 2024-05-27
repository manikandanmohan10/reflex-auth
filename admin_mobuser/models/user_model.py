from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    email: EmailStr
    password: str
    phone_number: str


class Login(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    email: EmailStr
    exp: int  # Token expiration time


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str