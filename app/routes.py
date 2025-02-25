from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.admin.routes import router as admin_router
from app.user.routes import router as user_router
from app.main_page.routes import router as main_page_router


def setup_routes(app: FastAPI):
    app.mount("/static", StaticFiles(directory="../static"), name="static")

    app.include_router(admin_router)

    app.include_router(user_router)
    app.include_router(main_page_router)
