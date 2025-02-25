import json
from http.client import HTTPResponse
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Depends
from fastapi.params import Body
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response, RedirectResponse

from app.admin.accessor import validate_admin
from app.utils.cookies_session import get_current_admin, COOKIE_NAME, get_admin_token
from app.utils.utils import templates

router = APIRouter(
    prefix="/admin"
)

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request, "title": "Главная"})

@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, response: Response, username: Annotated[str, Body()], password: Annotated[str, Body()]):
    admin = await validate_admin(username, password)
    if admin:
        token = get_admin_token(response, admin.id)
        response.set_cookie(key = COOKIE_NAME, value = str(token))
    else:
        raise HTTPException(status_code=403)
    return {'ok':True}

@router.get("/getme", response_class=HTMLResponse)
async def getme(request: Request, admin = Depends(get_current_admin)):
    return "ok"
