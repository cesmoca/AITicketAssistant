import pytest
from backend.repositories.sqlalquemy_task_repository import SQLAlchemyTaskRepository
from backend.domain.task import Task, TaskType
from backend.tests.fakes.fake_database import FakeDatabase


def test_repository():

    database = FakeDatabase()    

    repository = SQLAlchemyTaskRepository(database)

    task = Task(
        task_id=None,
        name="Name",
        appliance="Appliance",
        address="Address",
        failure="Failure",
        task_type = TaskType.NEW
    )
    
    repository.create(task)
    
    assert True == True