import pytest

from backend.domain.ticket_action import TicketAction, TicketActionType
from backend.processors.ai_ticket_processor import AITicketProcessor, ProcessTicketResult
from backend.tests.fakes.fake_ticket_ai import FakeTicketAI
from backend.tests.fakes.fake_ticket_repository import FakeTicketRepository


@pytest.fixture
def ticket_ai():
    yield FakeTicketAI()

@pytest.fixture
def repository():
    yield FakeTicketRepository()

@pytest.fixture
def processor(ticket_ai, repository):
    yield AITicketProcessor(repository=repository,ticket_ai=ticket_ai)


def test_process_ticket(processor: AITicketProcessor, ticket_ai, repository) -> ProcessTicketResult:
    ticket_ai.test_ticket = TicketAction(
        ticket_id=None,
        name="Name",
        appliance="Appliance",
        address="Address",
        failure="Failure",
        other_details="Other details",
        ticket_type = TicketActionType.NEW
    )
    
    result = processor.process_ticket("Some ticket")
    
    assert result.result is not None
    assert result.result.name == ticket_ai.test_ticket.name
    
    