from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/dashboard")
def dashboard(user=Depends(get_current_user)):
    return {
        "message": "Welcome to dashboard",
        "user": user["sub"]
    }
