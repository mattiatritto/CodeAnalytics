from fastapi.testclient import TestClient
from .app import app

client = TestClient(app)


def test_generate_report():
    report_data = {
        "cost": "5000.0",
        "duration": "30",
        "afp": "45.6",
        "start_date": "2024-10-30",
        "end_date": "2024-10-30",
        "today_date": "2024-10-30",
        "ei": "12",
        "eq": "5",
        "eo": "7",
        "ilf": "10",
        "eif": "8",
    }

    response = client.post("/generate_report/", json=report_data)
    assert response.status_code == 200
    assert (
        response.headers["content-type"]
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert "Content-Disposition" in response.headers