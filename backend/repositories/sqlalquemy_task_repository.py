from sqlalchemy.orm import DeclarativeBase
from .task_repository import TaskRepository

class SQLAlchemyBase(DeclarativeBase):
    pass

class SQLAlchemyTaskRepository(TaskRepository):

    def create(self, task: Task) -> Task:
        pass
    
    def update(self, task: Task):
        pass

    def get(self, id: int) -> Task | None:
        pass

    def list_tasks(self, type: Task.taskType | None) -> list(Task):
        pass