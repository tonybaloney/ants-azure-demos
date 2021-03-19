from functools import wraps
import azure.functions as az_functions
import json


def as_function(f):
    @wraps(f)
    def main(req: az_functions.HttpRequest) -> az_functions.HttpResponse:
        kwargs = req.route_params
        response = f(**kwargs)
        if isinstance(response, dict):
            response = json.dumps(response)
        return az_functions.HttpResponse(
            response,
            status_code=200,
        )

    return main
