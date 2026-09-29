import pytest
from backend.tests.utils.tickets_list import cases
from backend.remote.openai_task_ai import OpenAITaskAI
from backend.constants import SYSTEM_PROMPT, MODEL

@pytest.fixture
def task_ai():
    return OpenAITaskAI(SYSTEM_PROMPT, model=MODEL)

@pytest.mark.parametrize("case", cases)
def test_task_ai(task_ai, case):
    assert True