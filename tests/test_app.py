from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_welcome_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the ML API"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_model_correct_prediction():
    response = client.post(
        "/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )
    assert response.json() == {"prediction": "setosa"}


def test_model_wrong_input():
    response = client.post(
        "/predict",
        json={
            "sepal_length": 5.1,
        },
    )
    print(response.json())
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"


def test_nonexistent_endpoint():
    response = client.get("/nonexistent-path")
    assert response.status_code == 404
