from fastapi.testclient import TestClient
from backend.main import app
from backend.tests.fakes.fake_ticket_processor import FakeTicketProcessor

client = TestClient(app)

def test_endopoint_process_ticket():
    app.ticket_processor = FakeTicketProcessor()
    response = client.post(
        "/processTicket",
        json={ "text": "I am fed up!"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["ticket_id"] == 1
    assert data["result"]["info"]["name"] == "Pedro"
    assert data["result"]["info"]["address"] == "Calle agua"
    assert data["result"]["info"]["appliance"] == "Antena"
    assert data["result"]["info"]["failure"] == "FAKE: I am fed up!"
    assert data["result"]["info"]["other_details"] == "Tiene prisa"
    assert data["result"]["ticket_type"] == "new"

