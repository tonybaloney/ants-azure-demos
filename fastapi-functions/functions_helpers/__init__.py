from inspect import Parameter, Signature
from typing import Callable, Coroutine, Any
import azure.functions as az_functions
from fastapi.applications import FastAPI
import ujson as json
import fastapi
import asyncio


class FastApiWrapper:
    """
    Converts a FastAPI route into a "function object" that Azure Functions
    worker will use to call incoming HTTP requests.
    """

    def __init__(self, f: Callable, app: fastapi.FastAPI) -> None:
        self.f = f
        self.app = app

    def __call__(self, req: az_functions.HttpRequest) -> az_functions.HttpResponse:
        kwargs = req.route_params
        response = self.f(**kwargs)

        if isinstance(response, dict):
            response = json.dumps(response)

        return az_functions.HttpResponse(
            response,
            status_code=200,
        )

    @property
    def __annotations__(self):
        # TODO : Be clever about the annotations based on FastAPI specs
        return self.f.__annotations__

    @property
    def __signature__(self):
        """
        Pretend this function only has 1 arg(req) but at calltime it will leverage
        the request object.
        """
        return Signature(parameters=(Parameter(name="req", kind=1),))


class FastApiAsyncWrapper(FastApiWrapper):
    def __init__(self, f: Coroutine, app: fastapi.FastAPI) -> None:
        self.f = f
        self.app = app

    def __call__(self, req: az_functions.HttpRequest) -> az_functions.HttpResponse:
        kwargs = req.route_params
        query_args = req.params
        kwargs = kwargs | query_args
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(self.f(**kwargs))

        if isinstance(response, dict):
            response = json.dumps(response)

        return az_functions.HttpResponse(
            response,
            status_code=200,
        )


def as_function(f: Callable, app: FastAPI):
    return FastApiWrapper(f, app)


def coro_as_function(f: Coroutine, app: FastAPI):
    return FastApiAsyncWrapper(f, app)
