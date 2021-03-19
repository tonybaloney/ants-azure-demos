import fastapi
from functions_helpers import as_function
import mimesis

app = fastapi.FastAPI()


@app.get("/users/{user_id}")
def read_item(user_id: int):
    fake_user = mimesis.Person()
    return {
        "user_id": user_id,
        "username": fake_user.username(),
        "fullname": fake_user.full_name(),
        "age": fake_user.age(),
        "firstname": fake_user.first_name(),
        "lastname": fake_user.last_name(),
    }


main = as_function(read_item)
