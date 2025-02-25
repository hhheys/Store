import json
from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Body
from starlette.requests import Request
from starlette.responses import Response

from app.user.accessor import create_user, validate_user
from app.utils.cookies_session import COOKIE_NAME, send_user_cookie
from app.utils.utils import templates

router = APIRouter(
    prefix="/user"
)

@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("user_registration.html", {"request": request, "title": "Главная"})

@router.post("/register")
async def register(request: Request, response: Response, username: Annotated[str, Body()], phone_number: Annotated[str, Body()], password: Annotated[str, Body()]):
    data = await create_user(username, phone_number, password)
    if data:
        token = send_user_cookie(response, data.id)
        response.delete_cookie(COOKIE_NAME)
        response.set_cookie(key = COOKIE_NAME, value = str(token))
        return {
            'ok':True,
            'user': {
                'username': data.username,
                'phone_number': data.phone_number,
            }
        }
    else:
        return HTTPException(status_code=409)

@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("user_login.html", {"request": request})

@router.post("/login")
async def login(request: Request, response: Response, username: Annotated[str, Body()], password: Annotated[str, Body()]):
    user = await validate_user(username, password)
    if user:
        token = send_user_cookie(response, user.id)
        response.delete_cookie(COOKIE_NAME)
        response.set_cookie(key=COOKIE_NAME, value=str(token))
        return {
            'ok':True,
            'user': {
                'username': user.username,
                'phone_number': user.phone_number,
            }
        }
    else:
        return {
            'ok': False,
        }



