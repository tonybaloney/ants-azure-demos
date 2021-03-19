import fastapi
from functions_helpers import as_function


app = fastapi.FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


main = as_function(read_item)
