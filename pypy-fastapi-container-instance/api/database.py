from typing import List

from .db_models import DBLocation, DBUser
from .models import Location, User


async def create_user(name: str, email: str, password: str):
    await DBUser.create(name=name, email=email, password=password)

 
async def get_user(email: str) -> User:
    return await User.from_queryset_single(DBUser.get(email=email))


async def authenticate_user(email: str, password: str) -> bool:
    user = await User.from_queryset_single(
        DBUser.get(email=email, password=password)
    )

    if not user:
        return False
    else:
        return True


async def get_locations() -> List[Location]:
    return await Location.from_queryset(DBLocation.all())


async def add_location(name: str, private: bool):
    await DBLocation.create(name=name, private=private)
