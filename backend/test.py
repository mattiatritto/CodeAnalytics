from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_data():
    response = client.get("/data")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"




def test_predict():
    input_data = {
        "ilf_count": 5,
        "eif_count": 3,
        "ei_count": 10,
        "eo_count": 7,
        "eq_count": 4,
        "ilf_weight": 7,
        "eif_weight": 6,
        "ei_weight": 5,
        "eo_weight": 8,
        "eq_weight": 7,
        "gsc_values": [
            3,
            4,
            2,
            5,
            4,
            3,
            2,
            1,
            4,
            3,
            2,
            4,
            3,
            5,
        ],  # 14 values between 0 and 5
        "hourly_pay": 50,
        "effort": 100,
    }

    response = client.post("/predict", json=input_data)
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data[0], float)
    assert isinstance(response_data[1], float)
