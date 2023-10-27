import os
import sys

sys.path.append('./')

from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


def create_tables():
    Base.metadata.create_all(bind=engine)


def configure_cors(app):
    origins = settings.ORIGIN

    app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


def include_router(app):
    app.include_router(api_router)


def configure_staticfiles(app):
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(parent_dir,"images")): os.makedirs(os.path.join(parent_dir,"images"))
    app.mount("/images", StaticFiles(directory=os.path.join(parent_dir,"images")), name="images")
    app.mount("/static", StaticFiles(directory="static"), name="static")


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    configure_cors(app)
    include_router(app)
    configure_staticfiles(app)
    return app


app = start_application()


@app.get("/")
def home():
    return {"msg": "Hello FastAPI🚀"}

