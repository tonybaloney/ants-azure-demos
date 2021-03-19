import azure.functions as func
import helloWorld


def test_basic():
    req = func.HttpRequest(
        method="GET", url="items/2", body=b"", route_params={"item_id": "2"}
    )
    result = helloWorld.main(req)
    assert result.status_code == 200
    assert result.get_body().decode() == '{"item_id": "2"}'
