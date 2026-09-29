import pytest
from backend.tests.utils.tickets_list import cases
from backend.remote.openai_task_ai import OpenAITaskAI
@pytest.mark.parametrize("case", cases)


def test_task_ai(case):
    result = task_ai