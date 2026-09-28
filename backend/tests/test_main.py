from fastapi.testclient import TestClient
from backend.main import app
from backend.tests.fakes.fake_task_processor import FakeTaskProcessor

client = TestClient(app)

def test_endopoint_process_task():
    response = client.post(
        "/processTask",
        json={ "text": "I am fed up!"}
    )
    
    assert response.status_code == 200
    data = response.json()
    data["result"] == "FAKE: I am fed up!"
    
def test_fake_task_processor():
    fake_task_processor = FakeTaskProcessor()
    output = fake_task_processor.process_task("test")
    assert output == "FAKE: test"