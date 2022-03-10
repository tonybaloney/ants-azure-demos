from .main import app


@app.get("/", response_model=str, response_model_by_alias=False)
async def get_home(
) -> str:
    """
    Get all Todo lists
    Optional arguments:
    - **top**: Number of lists to return
    - **skip**: Number of lists to skip
    """
    return "Hello World!"