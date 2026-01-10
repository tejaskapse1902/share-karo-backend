from fastapi import APIRouter, HTTPException
from app.schemas.auth import SignupSchema, LoginSchema
from app.schemas.auth import ForgotPasswordSchema, VerifyOtpSchema, ResetPasswordSchema
from app.db.mongodb import user_collection
from app.core.security import create_access_token
from app.utils.emails import send_otp_email
from app.utils.otp import generate_otp
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/signup")
async def signup(data: SignupSchema):
    user = await user_collection.find_one({"email": data.email})
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    await user_collection.insert_one({
        "email": data.email,
        "name": data.name,
        "password": data.password
    })

    return {"message": "User registered successfully"}

@router.post("/login")
async def login(data: LoginSchema):
    user = await user_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not data.password == user["password"]:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/forgetpassword")
async def forget_password(data: ForgotPasswordSchema):
    email = data.email

    user = await user_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = generate_otp()
    expiry = datetime.utcnow() + timedelta(minutes=5)

    await user_collection.update_one(
        {"email": email},
        {"$set": {"otp": otp, "otp_expiry": expiry}}
    )

    send_otp_email(email, otp)

    return {"message": "OTP sent successfully"}


@router.post("/verifyotp")
async def verify_otp(data: VerifyOtpSchema):
    email = data.email
    otp = data.otp
    user = await user_collection.find_one({"email": email})

    if not user or user.get("otp") != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if user["otp_expiry"] < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    return {"message": "OTP verified"}


@router.post("/resetpassword")
async def reset_password(data: ResetPasswordSchema):
    email = data.email
    new_password = data.new_password

    await user_collection.update_one(
        {"email": email},
        {
            "$set": {"password": new_password},
            "$unset": {"otp": "", "otp_expiry": ""}
        }
    )

    return {"message": "Password reset successfully"}

@router.post("/logout")
def logout():
    response = JSONResponse({"message": "logged out"})
    response.delete_cookie("access_token")
    return response