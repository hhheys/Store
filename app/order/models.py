from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.price.models import Price
from app.products.models import Product
from app.user.models import User


@dataclass
class Position:
    product: Product
    price: Price

@dataclass
class Order:
    id: int
    positions: List[Position]
    user: User
    address: str
    date: datetime
    status: str



