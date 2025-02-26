from fastapi import APIRouter
from starlette.requests import Request

from app.user.routes import router
from app.utils.utils import templates

router = APIRouter(
    prefix=""
)

@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})