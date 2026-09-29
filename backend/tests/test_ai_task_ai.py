from pprint import pprint

import pytest

from backend.constants import MODEL, SYSTEM_PROMPT
from backend.remote.openai_task_ai import OpenAITaskAI
from backend.tests.utils.tickets_list import cases

def normalize(value: str | None) -> str | None:
    return value.strip().lower() if value is not None else None

@pytest.fixture
def task_ai():
    return OpenAITaskAI(SYSTEM_PROMPT, model=MODEL)


@pytest.mark.parametrize("case", cases)
def test_task_ai(task_ai, case):
    task = task_ai.request_ai(case["input"])

    print("> TASK ANSWER")
    pprint(task.model_dump_json(indent=2))
    print("> CASE")
    pprint(case)

    assert normalize(task.name) == normalize(case["expected_name"])
    assert normalize(task.address) == normalize(case["expected_address"])
    assert normalize(task.appliance) == normalize(case["expected_appliance"])
    assert normalize(task.failure) == normalize(case["expected_failure"])
    assert normalize(task.task_type) == normalize(case["expected_type"])
