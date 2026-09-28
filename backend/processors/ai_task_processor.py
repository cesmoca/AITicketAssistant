from .task_processor import TaskProcessor

class AITaskProcessor(TaskProcessor):
    
    def __init__(self, repository, task_ai):
        self.repository = repository 
        self.task_ai = task_ai
    
    def process_task(self, input: str) -> Task:
        task = self.task_ai.request_ai(input)
        
        # TODO here goes the persistance logic
        
        return task
        
    