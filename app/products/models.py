from pydantic.dataclasses import dataclass

from app.category.models import Category


@dataclass
class Product:
    id: int
    name: str
    description: str
    manufacturer_id: int
    category_id: int
    image_filename: str