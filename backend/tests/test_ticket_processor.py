import pytest

from backend.domain.task_info import TaskInfo
from backend.domain.ticket import Ticket
from backend.domain.ticket_action import TicketAction, TicketActionType
from backend.processors.ai_ticket_processor import AITicketProcessor
from backend.processors.ticket_processor import ProcessTicketRequest
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


def test_process_ticket(processor: AITicketProcessor, ticket_ai, repository):
    ticket_ai.test_ticket = TicketAction(
        info=TaskInfo(
            name="Name",
            appliance="Appliance",
            address="Address",
            failure="Failure",
            other_details="Other details",
        ),
        action_type = TicketActionType.NEW
    )

    request = ProcessTicketRequest(text="Some ticket")
    result = processor.process_ticket(request)

    assert ticket_ai.last_request is request
    assert result.status == "ok"
    assert result.data == "Ticket added"

    assert isinstance(result.result, Ticket)
    assert result.result.info.name == ticket_ai.test_ticket.info.name



@pytest.mark.parametrize("action_type", [TicketActionType.UPDATE, TicketActionType.CANCEL])
def test_resolution_required_has_null_data(processor, ticket_ai, action_type):
    ticket_ai.test_ticket = TicketAction(
        action_type=action_type,
        info=TaskInfo(name=None, appliance=None, address=None, failure=None, other_details=None),
    )
    request = ProcessTicketRequest(text="Ambiguous ticket")
    result = processor.process_ticket(request)

    assert ticket_ai.last_request is request
    assert result.data is None
    assert result.model_dump() == {"status": "resolution_required", "data": None, "result": None}
