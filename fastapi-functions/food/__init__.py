from functions_helpers import as_function
import mimesis
from api_app import app  # Our main API application


@app.get("/food/{food_id}")
def get_food(food_id: int):
    food = mimesis.Food()
    return {
        "food_id": food_id,
        "vegetable": food.vegetable(),
        "dish": food.dish(),
        "drink": food.drink(),
    }


main = as_function(get_food, app)
