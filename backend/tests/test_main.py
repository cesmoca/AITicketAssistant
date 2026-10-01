from fastapi.testclient import TestClient

from backend.main import app
from backend.tests.fakes.fake_ticket_processor import FakeTicketProcessor

client = TestClient(app)

def test_endopoint_process_ticket(monkeypatch):
    monkeypatch.setattr(app, "ticket_processor", FakeTicketProcessor())
    response = client.post(
        "/processTicket",
        json={ "text": "I am fed up!"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["id"] == 1
    assert data["result"]["info"]["name"] == "Pedro"
    assert data["result"]["info"]["address"] == "Calle agua"
    assert data["result"]["info"]["appliance"] == "Antena"
    assert data["result"]["info"]["failure"] == "FAKE: I am fed up!"
    assert data["result"]["info"]["other_details"] == "Tiene prisa"
    assert data["result"]["status"] == "active"
    assert data["status"] == "ok"
    assert data["data"] is None




def test_endpoint_list_tickets(monkeypatch):
    from backend.main import repository
    from backend.processors.ticket_processor import ProcessTicketRequest

    ticket = FakeTicketProcessor().process_ticket(ProcessTicketRequest(text="List fixture")).result
    monkeypatch.setattr(repository, "list", lambda: [ticket])
    response = client.get("/listTickets")

    assert response.status_code == 200
    assert response.json() == {"list": [ticket.model_dump(mode="json")]}
