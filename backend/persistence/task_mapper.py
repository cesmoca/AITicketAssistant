from enum import StrEnum
from ..domain.task import Task, TaskType
from task_entity import TaskEntity


class TaskMapper:
    
    def to_entity(self, task: Task) -> TaskEntity:
        return TaskEntity(
        id = task.id,
        name = task.name,
        appliance = task.appliance,
        address = task.address,
        failure = task.failure,
        task_type = task.task_type.value,
        )
    
    def to_domain(self, entity: TaskEntity) -> Task:
        return Task(
        id = entity.id,
        name = entity.name,
        appliance = entity.appliance,
        address = entity.address,
        failure = entity.failure,
        task_type = TaskType(entity.task_type)
        )