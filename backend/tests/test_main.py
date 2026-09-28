from fastapi.testclient import TestClient
from backend.main import app
from backend.tests.fakes.fake_task_processor import FakeTaskProcessor

client = TestClient(app)

def test_endopoint_process_task():
    app.task_processor = FakeTaskProcessor()
    response = client.post(
        "/processTask",
        json={ "text": "I am fed up!"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["task_id"] == 1
    assert data["result"]["name"] == "Pedro"
    assert data["result"]["address"] == "Calle agua"
    assert data["result"]["appliance"] == "Antena"
    assert data["result"]["failure"] == "FAKE: I am fed up!"
    assert data["result"]["task_type"] == "new"

