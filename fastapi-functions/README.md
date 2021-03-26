# FastAPI on Azure Functions

This is a basic FastAPI application running on Azure Functions FaaS. 

This demo would support FastAPI's full stack and instantiates Starlette's ASGI server framework.

## Layout

- The FastAPI app service is instantiated inside `api_app/`
- The app routes are defined in `app/`, there are two examples, `users/{id}` and `food/{id}`
- The Azure Functions descriptor allows all routes and HTTP verbs, since the routing is handled by FastAPI
- The ASGI adaptor is in `app/http_asgi.py`, you could reuse this code in other projects

## The ASGI endpoint

This application works by wrapping the FastAPI ASGI application in small, ASGI service that sends/receives Azure Functions Worker HTTPRequest/HTTPResponse Objects.

