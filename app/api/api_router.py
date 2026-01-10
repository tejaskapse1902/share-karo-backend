from fastapi import APIRouter
from app.api.routes import auth, protected
from app.api.routes import categories, reports, google_auth

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(protected.router, tags=["Protected"])
api_router.include_router(categories.router, tags=["Categories"])
api_router.include_router(reports.router, tags=["Reports"])
api_router.include_router(google_auth.router, tags=["Google OAuth"])