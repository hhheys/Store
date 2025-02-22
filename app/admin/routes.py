import json
from http.client import HTTPResponse
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response, RedirectResponse

from app.admin.accessor import validate_admin
from app.utils.cookies_session import send_admin_cookie, get_current_admin
from app.utils.utils import templates

router = APIRouter(
    prefix=""
)

@router.get("/admin/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request, "title": "Главная"})

@router.post("/admin/login", response_class=HTMLResponse)
async def login(request: Request, response: Response, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    admin = await validate_admin(username, password)
    if admin:
        send_admin_cookie(response, admin.id)
        print("cookie sended")
    else:
        raise HTTPException(status_code=403)

@router.get("/admin/getme", response_class=HTMLResponse)
async def getme(request: Request, admin = Depends(get_current_admin)):
    return "ok"
