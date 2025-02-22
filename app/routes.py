from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.admin.routes import router


def setup_routes(app: FastAPI):
    app.mount("/static", StaticFiles(directory="../static"), name="static")

    app.include_router(router)