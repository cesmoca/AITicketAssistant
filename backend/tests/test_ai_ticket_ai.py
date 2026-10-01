from pprint import pprint

import pytest

from backend.constants import MODEL, SYSTEM_PROMPT
from backend.remote.openai_ticket_ai import OpenAITicketAI
from backend.tests.utils.tickets_list import cases

def normalize(value: str | None) -> str | None:
    return value.strip().lower() if value is not None else None

@pytest.fixture
def ticket_ai():
    return OpenAITicketAI(SYSTEM_PROMPT, model=MODEL)


@pytest.mark.parametrize("case", cases)
def test_ticket_ai(ticket_ai, case):
    ticket = ticket_ai.request_ai(case["input"])

    print("> TICKET ANSWER")
    pprint(ticket.model_dump_json(indent=2))
    print("> CASE")
    pprint(case)

    assert normalize(ticket.info.name) == normalize(case["expected_name"])
    assert normalize(ticket.info.address) == normalize(case["expected_address"])
    assert normalize(ticket.info.appliance) == normalize(case["expected_appliance"])
    assert normalize(ticket.info.failure) == normalize(case["expected_failure"])
    assert normalize(ticket.ticket_type) == normalize(case["expected_type"])
