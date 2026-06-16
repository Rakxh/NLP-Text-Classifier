from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict():
    payload = {"texts": ["This product is amazing and works great."]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "predictions" in body
    assert len(body["predictions"]) == 1
    assert "label" in body["predictions"][0]
    assert "confidence" in body["predictions"][0]


def test_predict_batch():
    payload = {
        "texts": [
            "I love this, it works perfectly.",
            "It broke immediately, terrible quality.",
            "It is fine, nothing special.",
        ]
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert len(body["predictions"]) == 3
