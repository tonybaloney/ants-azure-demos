from typing import List

import mimesis

from .database import get_locations, add_location, create_user, authenticate_user
from .main import app
from .models import Location, LocationCreate, LoginRequest, UserCreate


@app.get("/locations", response_model=List[Location])
async def list_locations() -> List[Location]:
    return await get_locations()


@app.post("/locations")
async def add_location_(location: LocationCreate):
    await add_location(name=location.name, private=location.private)


@app.post("/register")
async def register(user: UserCreate):
    await create_user(user.name, user.email, user.password)
    return {"message": "User created successfully."}


@app.post("/login")
async def login(login: LoginRequest):
    if await authenticate_user(login.email, login.password):
        return {"message": "User login successful."}
    else:
        return {"message": "User login failed."}


@app.post("/seed")
async def seed(number: int):
    for _ in range(number):
        loc = mimesis.Address()
        await add_location(name=loc.address(), private=False)
        user = mimesis.Person()
        await create_user(
            name=user.full_name(), email=user.email(), password=user.password()
        )
