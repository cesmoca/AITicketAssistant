import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.repositories.sqlalquemy_task_repository import SQLAlchemyTaskRepository
from backend.domain.task import Task, TaskType
from backend.persistence.task_entity import TaskEntity
from backend.persistence.task_mapper import TaskMapper
from backend.tests.fakes.fake_database import FakeDatabase
from backend.persistence.sqlalchemy_base import SQLAlchemyBase


@pytest.fixture
def repository():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    
    SQLAlchemyBase.metadata.create_all(engine)
    
    TestSessionLocal = sessionmaker(bind=engine)

    repository = SQLAlchemyTaskRepository(
        session_factory=TestSessionLocal
    )
    
    task = Task(
        task_id=None,
        name="Name",
        appliance="Appliance",
        address="Address",
        failure="Failure",
        task_type = TaskType.NEW
    )
    
    yield repository
    
    SQLAlchemyBase.metadata.drop_all(engine)
        
@pytest.fixture
def task():

    task = Task(
        task_id=None,
        name="Name",
        appliance="Appliance",
        address="Address",
        failure="Failure",
        task_type = TaskType.NEW
    )
    
    yield task
        
def test_create(repository, task):
    
    repository.create(task)
    
    with repository.session_factory() as session:
        entity = session.get(TaskEntity, 1)
        
    assert entity is not None    
    assert entity.task_id == 1
    assert entity.name == task.name
    assert entity.appliance == task.appliance
    assert entity.address == task.address
    assert entity.failure == task.failure
    assert entity.task_type == task.task_type

    
def test_get_existing(repository, task):
    
    task.task_id = 5
    
    with repository.session_factory() as session:
        session.add(TaskMapper.to_entity(task))
        session.commit();
        
    get_task = repository.get(task.task_id)
    
    assert get_task is not None
    assert get_task.task_id == task.task_id
    assert get_task.name == task.name
    assert get_task.appliance == task.appliance
    assert get_task.address == task.address
    assert get_task.failure == task.failure
    assert get_task.task_type == task.task_type
    
def test_get_missing(repository, task):
    
    task.task_id = 5
    
    with repository.session_factory() as session:
        session.add(TaskMapper.to_entity(task))
        session.commit();
        
    get_task = repository.get(999)
    
    assert get_task is None
        
def test_list(repository, task):
    task.task_id = 5
    
    with repository.session_factory() as session:
        task.task_id = 1
        session.add(TaskMapper.to_entity(task))
        task.task_id = 2
        session.add(TaskMapper.to_entity(task))
        task.task_id = 3
        session.add(TaskMapper.to_entity(task))
        session.commit();
        
    tasks_list = repository.list()
    assert len(tasks_list) == 3    
    assert tasks_list[0].task_id == 1
    assert tasks_list[1].task_id == 2
    assert tasks_list[2].task_id == 3

    assert True