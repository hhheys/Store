from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Body, Depends
from pydantic import BaseModel
from starlette.requests import Request

from app.category.accessor import get_category_by_id, create_category
from app.products.accessor import get_product_by_category
from app.utils.cookies_session import get_current_admin
from app.utils.utils import templates

router = APIRouter(
    prefix="/category",
)

class CategoryCreate(BaseModel):
    category_name: str

@router.get("")
async def category_by_id(cat_id:int):
    print(await get_category_by_id(cat_id))
    print(await get_product_by_category(cat_id))
    return {}

@router.get("/create")
async def create_category_template(request:Request, admin = Depends(get_current_admin)):
    return templates.TemplateResponse("create_category.html", {"request": request})

@router.post("/create")
async def create_category_api(request:Request, category_name: CategoryCreate, admin = Depends(get_current_admin)):
    res = await create_category(category_name.category_name)
    if not res:
        return {'ok': False}
    return {
        'ok': True,
        'category': res.name
    }

