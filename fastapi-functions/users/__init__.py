from functions_helpers import coro_as_function
import mimesis
from typing import Optional
from api_app import app  # Our main API application


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


main = coro_as_function(read_item, app)
