from fastapi import APIRouter
from starlette.requests import Request

from app.category.accessor import get_all_categories
from app.manufacturers.accessor import get_all_manufacturers
from app.utils.cookies_session import get_current_user
from app.utils.utils import templates

router = APIRouter(
    prefix=""
)

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("main.html",
                                      {"request": request,
                                       "current_user": await get_current_user(request),
                                       "categories": await get_all_categories(),
                                       "manufacturers": await get_all_manufacturers()
                                       })