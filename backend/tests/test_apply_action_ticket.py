from itertools import product
from unittest.mock import Mock

import pytest

from backend.domain.task_info import TaskInfo
from backend.domain.ticket import Ticket, TicketStatus
from backend.domain.ticket_action import TicketAction, TicketActionType
from backend.processors.ai_ticket_processor import AITicketProcessor

FIELDS = ("name", "appliance", "address", "failure", "other_details")
ORIGINAL = {
    "name": "Ana Garcia",
    "appliance": "Lavadora",
    "address": "Calle Uno 10",
    "failure": "No enciende",
    "other_details": "Falla por la noche",
}
UPDATE = {
    "name": "Pedro Lopez",
    "appliance": "Horno",
    "address": "Calle Dos 20",
    "failure": "Hace ruido",
    "other_details": "Falla por la manana",
}


@pytest.fixture
def processor():
    return AITicketProcessor(repository=Mock(), ticket_ai=Mock())


@pytest.fixture
def ticket():
    return Ticket(id=42, info=TaskInfo(**ORIGINAL), status=TicketStatus.SUSPENDED)


def assert_ticket(ticket, expected_info):
    assert ticket.info.model_dump() == expected_info
    assert ticket.id == 42
    assert ticket.status == TicketStatus.SUSPENDED


NULL_COMBINATIONS = []

for null_flags in product((False, True), repeat=len(FIELDS)):
    null_fields = dict(zip(FIELDS, null_flags))
    null_field_names = []

    for field, is_null in null_fields.items():
        if is_null:
            null_field_names.append(field)

    if null_field_names:
        case_name = "null=" + ",".join(null_field_names)
    else:
        case_name = "null=none"

    NULL_COMBINATIONS.append(pytest.param(null_fields, id=case_name))

@pytest.mark.parametrize("null_fields", NULL_COMBINATIONS)
def test_update_replaces_values_and_preserves_null_fields(processor, ticket, null_fields):
    """Cover all 32 combinations, including no nulls and all nulls."""
    update_info = {
        field: None if null_fields[field] else UPDATE[field]
        for field in FIELDS
    }
    expected = {
        field: ORIGINAL[field] if null_fields[field] else UPDATE[field]
        for field in FIELDS
    }
    action = TicketAction(action_type=TicketActionType.UPDATE, info=TaskInfo(**update_info))

    processor._applyActionTicket(action, ticket)

    assert_ticket(ticket, expected)


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("update_is_null", [False, True], ids=["new-value", "still-null"])
def test_update_when_original_field_is_null(processor, ticket, field, update_is_null):
    original = {**ORIGINAL, field: None}
    ticket.info = TaskInfo(**original)
    update_info = dict.fromkeys(FIELDS, None)
    update_info[field] = None if update_is_null else UPDATE[field]
    expected = {**original, field: update_info[field]}
    action = TicketAction(action_type=TicketActionType.UPDATE, info=TaskInfo(**update_info))

    processor._applyActionTicket(action, ticket)

    assert_ticket(ticket, expected)


@pytest.mark.parametrize("field", FIELDS)
def test_empty_string_is_an_explicit_update(processor, ticket, field):
    """An empty string is a supplied value, distinct from null."""
    update_info = dict.fromkeys(FIELDS, None)
    update_info[field] = ""
    action = TicketAction(action_type=TicketActionType.UPDATE, info=TaskInfo(**update_info))

    processor._applyActionTicket(action, ticket)

    assert_ticket(ticket, {**ORIGINAL, field: ""})
