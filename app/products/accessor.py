from itertools import product

from app.price.accessor import set_price
from app.products.models import Product
from app.store.database import db


async def get_products_by_category(category_id: int):
    res = await db.fetch("SELECT * FROM products WHERE category_id = $1", category_id)
    return [Product(**pr) for pr in res]

async def get_product_by_manufacturer(manufacturer_id: int):
    res = await db.fetch("SELECT * FROM products WHERE manufacturer_id = $1", manufacturer_id)
    return [Product(**pr) for pr in res]

async def create_product(name: str, description: str, manufacturer_id:id, category_id: int, image_filename: str, product_price: int) -> Product | None:
    try:
        res = await db.fetchrow("INSERT INTO products (name, description, manufacturer_id, category_id, image_filename) VALUES ($1, $2, $3, $4, $5) RETURNING *", name, description, manufacturer_id, category_id, image_filename)
        product_id = res["id"]
        pr = await get_product_by_id(product_id)
        await set_price(pr.id, product_price)
        return pr
    except Exception as e:
        print(e)
        return None

async def get_product_by_id(product_id: int) -> Product:
    res = await db.fetchrow("SELECT * FROM products WHERE id = $1", product_id)
    if res is not None:
        return Product(**res)

async def add_promotional_product(product_id: int):
    try:
        await db.execute("INSERT INTO promotional_items (product_id) VALUES ($1)", product_id)
    except Exception as e:
        print(e)
        return None
    return True

async def del_promotional_product(product_id: int):
    try:
        await db.execute("DELETE FROM promotional_items WHERE product_id = $1", product_id)
    except Exception as e:
        print(e)
        return None
    return True

async def get_all_promotional_products():
    res = await db.fetch("SELECT * FROM promotional_items")
    data = []
    for rec in res:
        product_id = rec.get("product_id")
        product = await get_product_by_id(product_id)
        data.append(product)
    return data