from typing import Annotated

from fastapi import APIRouter, Form, File, UploadFile
from fastapi.params import Body, Depends
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.manufacturers.accessor import get_manufacturer_by_id, create_manufacturer
from app.products.accessor import get_product_by_manufacturer
from app.utils.cookies_session import get_current_admin
from app.utils.utils import templates, save_image

router = APIRouter(
    prefix="/manufacturer",
)

class ManufacturerCreate(BaseModel):
    manufacturer_name: str

@router.get("")
async def manufacturer_by_id(man_id:int):
    print(await get_manufacturer_by_id(man_id))
    print(await get_product_by_manufacturer(man_id))
    return {}

@router.get("/create")
async def create_manufacturer_template(request:Request, admin = Depends(get_current_admin)):
    return templates.TemplateResponse("create_manufacturer.html", {"request": request})

@router.post("/create")
async def create_manufacturer_api(request:Request, manufacturer_name: Annotated[str, Form()], manufacturer_image: Annotated[UploadFile, File()], admin = Depends(get_current_admin)):
    image_filename = save_image(manufacturer_name, manufacturer_image)
    res = await create_manufacturer(manufacturer_name, image_filename)
    if res:
        return RedirectResponse("/", status_code=303)
    raise HTTPException(status_code=409)


