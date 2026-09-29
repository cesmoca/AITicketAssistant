from sqlalchemy.sql import select, delete
from .task_repository import TaskRepository
from ..domain.task import Task
from ..persistence.database import Database
from ..persistence.task_entity import TaskEntity 
from ..persistence.task_mapper import TaskMapper

class SQLAlchemyTaskRepository(TaskRepository):
        
    def __init__(self, session_factory):
        self.session_factory = session_factory
        
    def create(self, task: Task) -> Task:

        if task.task_id is not None:
            raise ValueError("Cannot create a Task that already has an ID")
        

        with self.session_factory() as session:

            entity = TaskMapper.to_entity(task)
            
            session.add(entity)
            session.commit()

            session.refresh(entity)

            return TaskMapper.to_domain(entity)
            

    def get(self, task_id: int) -> Task | None:
        statement = select(TaskEntity).where(TaskEntity.task_id == task_id)
        
        with self.session_factory() as session:
            entity = session.scalar(statement)
            
            if entity is None:
                return None

            return TaskMapper.to_domain(entity)
        
            
    def update(self, task: Task) -> Task:
        if task.task_id is None:
            raise ValueError("The task should have an id")
        
        statement = select(TaskEntity).where(TaskEntity.task_id == task.task_id)
        
        with self.session_factory() as session:
            old_entity = session.scalar(statement)
            if old_entity is None:
                raise ValueError(f"Could not find a Task with id {task.task_id}")
            
            TaskMapper.update_entity(old_entity, task)
            session.commit()
            session.refresh(old_entity)
            
            return TaskMapper.to_domain(old_entity)
            


    def list(self) -> list[Task]:
        statement = select(TaskEntity)
        
        with self.session_factory() as session:
            entities_list = session.scalars(statement=statement).all()
            return [TaskMapper.to_domain(entity) for entity in entities_list]
        
        
    def searchTask(self, task) -> list(Task):
        all_tasks: list[Task] = self.list()
        candidate_tasks = [candidate_task for candidate_task in all_tasks if self._areTasksSimilar(task, candidate_task)]
        return candidate_tasks
    
    def delete(self, task_id) -> Boolean:
        
        if task_id is None:
            raise ValueError("Delete should have a valid task_id")
        
        with self.session_factory() as session:
            task = session.get(TaskEntity, task_id)
            
            if task is None:
                return False
            
            session.delete(task)
            session.commit()
            
            return True
    
    def clear(self):
        with self.session_factory() as session:
            session.execute(delete(TaskEntity))
            session.commit()
        
    def _areTasksSimilar(self, task1: Task, task2: Task) -> list[Task]:
        if task1.name.strip().lower() == task2.name.strip().lower():
            return True
        
        if task1.address.strip().lower() == task2.address.strip().lower():
            return True
        
        return False
