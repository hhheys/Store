from app.price.accessor import set_price
from app.products.models import Product
from app.store.database import db


async def get_products_by_category(category_id: int):
    res = await db.fetch("SELECT * FROM products WHERE category_id = $1", category_id)
    return [Product(**pr) for pr in res]

async def get_product_by_manufacturer(manufacturer_id: int):
    res = await db.fetch("SELECT * FROM products WHERE manufacturer_id = $1", manufacturer_id)
    return [Product(**pr) for pr in res]

async def create_product(name: str, description: str, manufacturer_id: int, category_id: int, image_filename: str, product_price: int) -> Product | None:
    try:
        await db.execute("INSERT INTO products (name, description, manufacturer_id, category_id, image_filename) VALUES ($1, $2, $3, $4, $5)", name, description, manufacturer_id, category_id, image_filename)
    except Exception as e:
        print(e)
        return None
    pr = Product(**(await db.fetchrow("SELECT * FROM products WHERE name = $1", name)))
    try:
        await set_price(pr.id, product_price)
    except Exception as e:
        print(e)
    return pr

async def get_product_by_id(product_id: int) -> Product:
    res = await db.fetchrow("SELECT * FROM products WHERE id = $1", product_id)
    if res is not None:
        return Product(**res)