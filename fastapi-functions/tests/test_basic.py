import azure.functions as func
import helloWorld
import json


def test_basic():
    req = func.HttpRequest(
        method="GET", url="users/2", body=b"", route_params={"user_id": "2"}
    )
    result = helloWorld.main(req)
    assert result.status_code == 200
    assert json.loads(result.get_body().decode())["user_id"] == "2"
