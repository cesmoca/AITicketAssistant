from pprint import pprint
from .task_processor import TaskProcessor
from ..domain.task import Task, TaskType

class AITaskProcessor(TaskProcessor):
    
    def __init__(self, repository, task_ai):
        self.repository = repository 
        self.task_ai = task_ai
    
    def process_task(self, input: str) -> Task:
        task = self.task_ai.request_ai(input)
        pprint(task)
        
        if task.task_type == "new":
            self.repository.create(task)
            
        elif task.task_type == "update":
            candidates = self.repository.searchTask(task)
            
            if len(candidates) == 1:
                self._updateTask(task, candidates[0])
                self.repository.update(task)
                
        elif task.task_type == "cancel":
            candidates = self.repository.searchTask(task)
        else:
            pprint(f"Undetermined database action for task type: {task.task_type}")
            
        return task
    
    def _updateTask(self, toTask: Task, fromTask: Task):
        
        toTask.task_id = fromTask.task_id
        if toTask.name is None:
            toTask.name = fromTask.name
            
        if toTask.appliance is None:
            toTask.appliance = fromTask.appliance
            
        if toTask.address is None:
            toTask.address = fromTask.address
            
        if toTask.failure is None:
            toTask.failure = fromTask.failure
            
        
        
    