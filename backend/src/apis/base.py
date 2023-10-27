from apis.routes import route_upload
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(route_upload.router, prefix="", tags=["upload"])
