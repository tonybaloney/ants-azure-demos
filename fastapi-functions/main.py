import fastapi
import json

app = fastapi.FastAPI()


@app.get("/")
def index():
    return "Hello world!"

if __name__ == "__main__":
    with open('spec.json', 'w') as spec:
        spec.write(json.dumps(app.openapi(), indent=2))
