from enum import StrEnum
from ..domain.task import Task, TaskType
from .task_entity import TaskEntity


class TaskMapper:
    
    @staticmethod
    def to_entity(task: Task) -> TaskEntity:
        return TaskEntity(
        task_id = task.task_id,
        name = task.name,
        appliance = task.appliance,
        address = task.address,
        failure = task.failure,
        other_details = task.other_details,
        task_type = task.task_type.value,
        )
    
    @staticmethod
    def to_domain(entity: TaskEntity) -> Task:
        return Task(
        task_id = entity.task_id,
        name = entity.name,
        appliance = entity.appliance,
        address = entity.address,
        failure = entity.failure,
        other_details = entity.other_details,
        task_type = TaskType(entity.task_type)
        )
        
    @staticmethod
    def update_entity(entity: TaskEntity, task: Task) -> None:
        entity.name = task.name
        entity.appliance = task.appliance
        entity.address = task.address
        entity.failure = task.failure
        entity.other_details = task.other_details
        entity.task_type = task.task_type.value