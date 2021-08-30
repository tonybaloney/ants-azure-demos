from typing import Generic, List, TypeVar

from beanie import Indexed

T = TypeVar("T")

from beanie import Document
from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_connection: str
    mongo_db = "demo_app_db"


class Address(Document):
    street_number: int
    street_name: str
    city: str
    country: str
    longitude: float
    latitude: float
    postal_code: Indexed(str)  # We sort on postal codes, so index them

    class Collection:
        name = "addresses"


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
