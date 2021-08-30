from typing import Generic, List, Tuple, TypeVar

import pymongo
from beanie import Indexed

T = TypeVar("T")

from typing import Any

from beanie import Document
from pydantic import BaseModel, BaseSettings


class Settings(BaseSettings):
    mongo_connection: str
    mongo_db = "demo_app_db"


class GeoJson2DPoint(BaseModel):
    type: str = "Point"
    coordinates: Tuple[float, float]


class Address(Document):
    street_number: int
    street_name: str
    city: str
    country: str
    geo: GeoJson2DPoint
    postal_code: str

    class Collection:
        name = "addresses"
        indexes = [
            [("geo", pymongo.GEOSPHERE)],  # GEO index
            [("postal_code", pymongo.ASCENDING)],
        ]


class Paged(Generic[T]):
    items: List[T]
    size: int
    more_pages: bool

    def __init__(self, number: int, items: List[T], more_pages: bool):
        self.items = items
        self.number = number
        self.more_pages = more_pages


# All models to instantiate on load
__beanie_models__ = [Address]
