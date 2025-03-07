from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Form
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.cart.accessor import get_all_cart, del_all_cart
from app.order.accessor import add_new_order
from app.order.models import Order
from app.user.models import User
from app.utils.cookies_session import get_current_user
from app.warehouse.accessor import add_new_sale

router = APIRouter(
    prefix="/order",
)

class CreateOrder(BaseModel):
    address: str

@router.post("/create")
async def create_order_post(request: Request, address: Annotated[str, Form()], user: User = Depends(get_current_user)) -> Order:
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    cart = await get_all_cart(user.id)
    count = 0
    for item in cart:
        if item.count > 0:
            count += 1
    if count == 0:
        return RedirectResponse("/user", status_code=303)



    order_id = await add_new_order(user.id, address)
    cart = await get_all_cart(user.id)
    for product in cart:
        try:
            await add_new_sale(product.product.id, order_id.get("id"))
        except Exception as e:
            print(e)
            continue
    await del_all_cart(user.id)
    return RedirectResponse("/user", status_code=303)



