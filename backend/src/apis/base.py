from apis.routes import route_upload
from apis.routes import route_save
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(route_upload.router, prefix="", tags=["upload"])
api_router.include_router(route_save.router, prefix="", tags=["save"])
