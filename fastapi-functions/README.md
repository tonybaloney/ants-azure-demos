# FastAPI on Azure Functions

This is a basic FastAPI route inside Azure Functions with a wrapper that converts Azure Functions Runtime requests into a call to the FastAPI route.

## Layout

- Each REST resource would have a submodule. E.g., `/api/food/` lives inside the `food/` submodule
- Each resource/submodule describes its own `function.json`
- Route parameters are shared between the Azure Functions runtime and the FastAPI route declaration
- There is a shared "app" object for shared configuration (inside `api_app`)
- Azure Functions runtime will call a function object-shim created by `functions_helpers.as_function`

## The shim

This is a **quick prototype with lots of limitations** (I only had a couple of hours on Friday to work on it)

- Only tested with GET
- Only tested with route params, not URL params

## Unit tests

Added a pytest test example in `tests/` to show how this would be unit tested. 
