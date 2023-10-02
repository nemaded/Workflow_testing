import httpx
from main import app

def test_health_check():
    with httpx.Client(app=app, base_url="http://testserver") as client:
        response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}