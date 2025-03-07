from typing import List

from app.order.models import Order, Position
from app.price.accessor import get_price_for_date
from app.products.accessor import get_product_by_id
from app.store.database import db
from app.user.accessor import get_user_by_id


async def get_all_orders(user_id: int) -> List[Order]:
    res = await db.fetch("SELECT * FROM orders WHERE client_id=$1 ORDER BY date DESC LIMIT 3", user_id)
    orders = []
    for order in res:
        products = await db.fetch("SELECT * FROM sales WHERE order_id=$1", order['id'])
        positions = []
        for product in products:
            product = await get_product_by_id(product['product_id'])
            price = await get_price_for_date(product.id, order['date'])
            positions.append(Position(product=product, price=price))
        orders.append(Order(id = order['id'],
                            positions= positions,
                            user = await get_user_by_id(user_id),
                            address= order['address'],
                            date=order['date'],
                            status= "None"
                            ))
    return orders

async def get_order(order_id: int, user_id: int) -> Order:
    order = await db.fetchrow("SELECT * FROM orders WHERE client_id=$1 LIMIT 1", user_id)
    products = await db.fetch("SELECT * FROM sales WHERE order_id=$1", order['id'])
    positions = []
    for product in products:
        product = await get_product_by_id(product['product_id'])
        price = await get_price_for_date(product.id, order['date'])
        positions.append(Position(product=product, price=price))
    return Order(id=order['id'],
                        positions=positions,
                        user=await get_user_by_id(user_id),
                        address=order['address'],
                        date=order['date'],
                        status="None"
                        )

async def add_new_order(user_id: int, address: str) -> int:
    await db.execute("INSERT INTO orders (client_id, address) VALUES ($1, $2)", user_id, address)

    return await db.fetchrow("SELECT id FROM orders WHERE client_id=$1 ORDER BY date DESC LIMIT 1;", user_id)