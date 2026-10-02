from pathlib import Path

from backend.domain.task_info import TaskInfo
from backend.domain.ticket import TicketStatus
from evals.runner import load_dataset


INFO_FIELDS = set(TaskInfo.model_fields)
TICKET_FIELDS = INFO_FIELDS | {"id", "state"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_fields(fields: dict, label: str, *, selector: bool = False) -> None:
    require(isinstance(fields, dict), f"{label} must be an object")
    if selector:
        require(bool(fields), f"{label} must not be empty")
    require(not (fields.keys() - TICKET_FIELDS), f"{label} contains unknown ticket fields")
    for field, value in fields.items():
        if field in INFO_FIELDS:
            require(value is None or isinstance(value, str), f"{label}.{field} must be a string or null")
        elif field == "state":
            require(isinstance(value, str) and value in TicketStatus.__members__, f"{label}.state must be a TicketStatus name")
        elif field == "id":
            require(type(value) is int, f"{label}.id must be an integer")


def absent_selector(entry: dict) -> dict:
    return entry["match"] if isinstance(entry, dict) and set(entry) == {"match"} else entry


def validate_case(case: dict) -> None:
    require(isinstance(case.get("id"), str) and bool(case["id"].strip()), "id must be a non-empty string")
    require(isinstance(case.get("input"), str), "input must be a string")
    if "notes" in case:
        require(isinstance(case["notes"], str), "notes must be a string")

    setup = case.get("setup")
    require(isinstance(setup, dict), "setup must be an object")
    require(isinstance(setup.get("tickets"), list), "setup.tickets must be a list")
    for ticket in setup["tickets"]:
        validate_fields(ticket, "setup.tickets")
        require("state" in ticket, "setup tickets require state")
        require("id" not in ticket, "setup IDs are assigned by the repository")

    expected = case.get("expected")
    require(isinstance(expected, dict), "expected must be an object")
    response = expected.get("response")
    require(isinstance(response, dict), "expected.response must be an object")
    require(isinstance(response.get("status"), str), "expected.response.status must be a string")
    require("data" in response, "expected.response.data is required")
    require(response["data"] is None or isinstance(response["data"], str), "expected.response.data must be a string or null")
    database = expected.get("database")
    require(isinstance(database, dict), "expected.database must be an object")
    count = database.get("ticket_count")
    require(type(count) is int and count >= 0, "ticket_count must be a non-negative integer")
    require(isinstance(database.get("tickets"), list), "expected.database.tickets must be a list")
    for ticket in database["tickets"]:
        require(isinstance(ticket, dict), "expected ticket must be an object")
        validate_fields(ticket.get("match"), "match", selector=True)
        validate_fields(ticket.get("assert"), "assert")
    absent = database.get("absent", [])
    require(isinstance(absent, list), "expected.database.absent must be a list")
    for entry in absent:
        validate_fields(absent_selector(entry), "absent", selector=True)


def load_cases(source: Path) -> list[dict]:
    files = [source] if source.is_file() else sorted(source.rglob("*.jsonl"))
    require(bool(files), f"No JSONL datasets found at {source}")
    cases = []
    ids = set()
    for path in files:
        for case in load_dataset(path):
            try:
                validate_case(case)
                require(case["id"] not in ids, f"duplicate case ID: {case['id']}")
            except ValueError as error:
                raise ValueError(f"{path}, case {case.get('id', '?')}: {error}") from error
            ids.add(case["id"])
            cases.append({**case, "source": str(path)})
    return cases
