from pprint import pprint

import pytest

from backend.constants import MODEL, SYSTEM_PROMPT
from backend.domain.ticket_action import TicketAction
from backend.processors.ticket_processor import ProcessTicketRequest
from backend.remote.openai_ticket_ai import OpenAITicketAI
from backend.tests.utils.tickets_list import cases


def normalize(value: str | None) -> str | None:

    return value.strip().lower() if value is not None else None


@pytest.fixture
def ticket_ai():

    return OpenAITicketAI(SYSTEM_PROMPT, model=MODEL)


@pytest.mark.parametrize("case", cases)
def test_ticket_ai(ticket_ai, case):
    ticket_action = ticket_ai.request_ai(ProcessTicketRequest(text=case["input"]))
    assert isinstance(ticket_action, TicketAction)

    print("> TICKET ANSWER")
    pprint(ticket_action.model_dump_json(indent=2))

    print("> CASE")
    pprint(case)

    assert normalize(ticket_action.info.name) == normalize(case["expected_name"])

    assert normalize(ticket_action.info.address) == normalize(case["expected_address"])

    assert normalize(ticket_action.info.appliance) == normalize(
        case["expected_appliance"]
    )

    assert normalize(ticket_action.info.failure) == normalize(case["expected_failure"])

    assert normalize(ticket_action.action_type) == normalize(case["expected_type"])
