from typing import List

import mimesis
from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse

import example_app.database as database
from example_app.main import app, templates
from example_app.models import LoginRequest, UserCreate


@app.get("/locations", response_class=HTMLResponse)
async def list_locations(
    request: Request,
):
    locations = await database.get_locations()
    return templates.TemplateResponse(
        "locations.html", {"request": request, "locations": locations}
    )


@app.post("/register")
async def register(user: UserCreate):
    await database.create_user(user.name, user.email, user.password)
    return {"message": "User created successfully."}


@app.post("/login")
async def login(login: LoginRequest):
    if await database.authenticate_user(login.email, login.password):
        return {"message": "User login successful."}
    else:
        return {"message": "User login failed."}


@app.post("/seed")
async def seed(number: int):
    for _ in range(number):
        loc = mimesis.Address()
        await database.add_location(name=loc.address(), private=False)
        user = mimesis.Person()
        await database.create_user(
            name=user.full_name(), email=user.email(), password=user.password()
        )


@app.get("/")
def index():
    return "hello, world!"


@app.get("/bad_page")
def bad_page():
    total = 0
    for i in range(-5, 10):
        total += 5 / i  # will hit a ZeroDivisionError
    return total


@app.get("/native_error")
def bad_page2():
    raise HTTPException(status_code=500, detail="There was a big boo-boo.")
