from fastapi.testclient import TestClient

from ..app import app

client = TestClient(app)


def test_model_correct_positive_prediction():
    response = client.post("/predict", json={"text": "good job!"})
    assert response.json() == {"prediction": "positive"}


def test_model_correct_neutral_prediction():
    response = client.post("/predict", json={"text": "kochac morgula?"})
    assert response.json() == {"prediction": "neutral"}


def test_model_correct_negative_prediction():
    response = client.post(
        "/predict", json={"text": "you smelly little stupid muffin head"}
    )
    assert response.json() == {"prediction": "negative"}


def test_model_wrong_input_type():
    response = client.post("/predict", json={"text": 123})
    assert response.status_code == 422


def test_model_empty_string_input():
    response = client.post("/predict", json={"text": ""})
    assert response.json()["message"] == "Invalid or empty string"
    assert response.status_code == 422


def test_model_wrong_input_parameter():
    response = client.post("/predict", json={"XD": 123})
    assert response.json()["detail"][0]["type"] == "missing"
    assert response.status_code == 422
