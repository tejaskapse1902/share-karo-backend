from pydantic import BaseModel, EmailStr

class SignupSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class VerifyOtpSchema(BaseModel):
    email: EmailStr
    otp: str
    
class ResetPasswordSchema(BaseModel):
    email: EmailStr
    new_password: str

class GoogleLoginSchema(BaseModel):
    id_token: str