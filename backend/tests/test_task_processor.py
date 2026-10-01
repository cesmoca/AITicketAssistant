import pytest

from backend.domain.task_action import TaskAction, TaskActionType
from backend.processors.ai_task_processor import AITaskProcessor, ProcessTaskResult
from backend.tests.fakes.fake_task_ai import FakeTaskAI
from backend.tests.fakes.fake_task_repository import FakeTaskRepository


@pytest.fixture
def task_ai():
    yield FakeTaskAI()

@pytest.fixture
def repository():
    yield FakeTaskRepository()

@pytest.fixture
def processor(task_ai, repository):
    yield AITaskProcessor(repository=repository,task_ai=task_ai)


def test_process_task(processor: AITaskProcessor, task_ai, repository) -> ProcessTaskResult:
    task_ai.test_task = TaskAction(
        task_id=None,
        name="Name",
        appliance="Appliance",
        address="Address",
        failure="Failure",
        other_details="Other details",
        task_type = TaskActionType.NEW
    )
    
    result = processor.process_task("Some ticket")
    
    assert result.result is not None
    assert result.result.name == task_ai.test_task.name
    
    