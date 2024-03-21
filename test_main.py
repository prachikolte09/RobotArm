import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.parametrize("width, height, length, mass, expected_result", [
    (10, 20, 30, 5, "STANDARD"),

])
def test_sort_package(width, height, length, mass, expected_result):
    response = client.post(
        "/sort_package/",
        json={"width": width, "height": height, "length": length, "mass": mass}
    )
    assert response.status_code == 200
    assert response.json()["result"] == expected_result
