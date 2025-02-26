from app.products.models import Product
from app.store.database import db


async def get_product_by_category(category_id: int):
    res = await db.fetch("SELECT * FROM products WHERE category_id = $1", category_id)
    return [Product(**pr) for pr in res]

async def create_product(name: str, description: str, manufacturer_id: int, category_id: int, image_filename: str) -> Product | None:
    try:
        await db.execute("INSERT INTO products (name, description, manufacturer_id, category_id, image_filename) VALUES ($1, $2, $3, $4, $5)", name, description, manufacturer_id, category_id, image_filename)
    except Exception as e:
        return None
    cat = await db.fetchrow("SELECT * FROM products WHERE name = $1", name)
    return Product(**cat)