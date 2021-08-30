from typing import Optional

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
    longitude: str
    latitude: str
    postal_code: Optional[str]

    class Collection:
        name = "addresses"


# All models to instantiate on load
__beanie_models__ = [Address]
