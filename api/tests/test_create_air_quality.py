from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_air_quality():
    air_quality_data = {
        "latitude": 1.2345,
        "longitude": 2.3456,
        "elevation": 100,
        "type_gas": "pm10",
        "data": [1, 2, 3, 4, 5],
        "tag": "Bogota"
    }

    response = client.post("/air_quality/api/data", json=air_quality_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Data created successfully"}
