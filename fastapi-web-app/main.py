import fastapi


app = fastapi.FastAPI()


@app.get("/")
def index():
    return "Hello world!"
