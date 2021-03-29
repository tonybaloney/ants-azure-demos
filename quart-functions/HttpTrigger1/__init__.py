import azure.functions as func
from .http_asgi import AsgiMiddleware
from quart import Quart, render_template, websocket
import logging
logging.basicConfig(level=logging.DEBUG)

app = Quart(__name__)


@app.route("/")
async def hello():
    return await render_template("index.html")


@app.route("/api")
async def json():
    return {"hello": "world"}


def main(req: func.HttpRequest, context: func.Context):
    return AsgiMiddleware(app).handle(req, context)
