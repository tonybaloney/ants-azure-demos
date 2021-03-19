import azure.functions as func
import users
import food
import json


def test_users():
    req = func.HttpRequest(
        method="GET", url="users/2", body=b"", route_params={"user_id": "2"}
    )
    result = users.main(req)
    assert result.status_code == 200
    assert json.loads(result.get_body().decode())["user_id"] == "2"


def test_food():
    req = func.HttpRequest(
        method="GET", url="food/2", body=b"", route_params={"food_id": "2"}
    )
    result = food.main(req)
    assert result.status_code == 200
    assert json.loads(result.get_body().decode())["food_id"] == "2"
