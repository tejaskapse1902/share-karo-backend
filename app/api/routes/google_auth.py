from fastapi import APIRouter, HTTPException
from app.services.google_oauth import exchange_code_for_token, get_google_user_info
from app.db.mongodb import user_collection
from app.core.security import create_access_token
import os

router = APIRouter()


@router.get("/auth/google/login")
def google_login_url():
    scope = "openid email profile"

    url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={os.getenv('GOOGLE_CLIENT_ID')}"
        f"&redirect_uri={os.getenv('GOOGLE_REDIRECT_URI')}"
        "&response_type=code"
        f"&scope={scope.replace(' ', '%20')}"
        "&access_type=offline"
        "&prompt=consent"
    )

    return {"login_url": url}



@router.get("/auth/google/callback")
async def google_callback(code: str):
    try:
        tokens = exchange_code_for_token(code)
        access_token = tokens["access_token"]

        google_user = get_google_user_info(access_token)

        email = google_user.get("email")
        name = google_user.get("name", "")

        if not email:
            raise HTTPException(status_code=400, detail="Email permission not granted by Google")

        user = await user_collection.find_one({"email": email})

        if not user:
            await user_collection.insert_one({
                "email": email,
                "username": name,
                "auth_provider": "google"
            })

        jwt_token = create_access_token({"sub": email})

        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "email": email
        }

    except Exception as e:
        print("GOOGLE CALLBACK ERROR:", e)
        raise HTTPException(status_code=400, detail=str(e))
