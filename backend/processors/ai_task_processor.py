from pprint import pprint
from .task_processor import TaskProcessor

class AITaskProcessor(TaskProcessor):
    
    def __init__(self, repository, task_ai):
        self.repository = repository 
        self.task_ai = task_ai
    
    def process_task(self, input: str) -> Task:
        task = self.task_ai.request_ai(input)
        
        if task.task_type == "new":
            self.repository.create(task)
            pprint("Created a new task")
            
        elif task.task_type == "update":
            candidate = self.repository.getTicketFromDB(task)
        
        elif task.task_type == "cancel":
            candidate = self.repository.getTicketFromDB(task)
        
        else:
            pprint(f"Undetermined database action for task type: {task.task_type}")
            
        return task
        
    