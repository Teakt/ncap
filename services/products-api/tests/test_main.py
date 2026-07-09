from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Product 1", "price": 19.99}, 
                               {"id": 2, "name": "Product 2", "price": 29.99}]
