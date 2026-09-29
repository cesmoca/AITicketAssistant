import pytest

from backend.processors.ai_task_processor import AITaskProcessor, ProcessTaskResult
from backend.domain.task import Task, TaskType
from backend.tests.fakes.fake_task_repository import FakeTaskRepository
from backend.tests.fakes.fake_task_ai import FakeTaskAI


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
    task_ai.test_task = Task(
        task_id=None,
        name="Name",
        appliance="Appliance",
        address="Address",
        failure="Failure",
        task_type = TaskType.NEW
    )
    
    result = processor.process_task("Some ticket")
    
    assert result.task is not None
    assert result.task.name == result.task_ai.test_task.name
    
    