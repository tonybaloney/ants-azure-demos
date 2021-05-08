import azure.functions as func
try:
    from azure.functions import AsgiMiddleware
except ModuleNotFoundError:
    from _future.azure.functions._http_asgi import AsgiMiddleware

import mimesis
from api_app import app  # Our main API application
from typing import Optional
from pydantic import BaseModel


class FoodItem(BaseModel):
    id: int
    vegetable: str
    dish: str
    drink: str


@app.get("/food/{food_id}")
async def get_food(
    food_id: int,
):
    food = mimesis.Food()
    return {
        "food_id": food_id,
        "vegetable": food.vegetable(),
        "dish": food.dish(),
        "drink": food.drink(),
    }


@app.post("/food/")
async def create_food(food: FoodItem):
    # Write the food item to the database here.
    return food


@app.get("/users/{user_id}")
async def read_item(user_id: int, locale: Optional[str] = None):
    fake_user = mimesis.Person(locale=locale)
    return {
        "user_id": user_id,
        "username": fake_user.username(),
        "fullname": fake_user.full_name(),
        "age": fake_user.age(),
        "firstname": fake_user.first_name(),
        "lastname": fake_user.last_name(),
    }


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AsgiMiddleware(app).handle(req, context)
