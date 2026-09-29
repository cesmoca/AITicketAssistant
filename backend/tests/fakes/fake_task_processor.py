from backend.processors.task_processor import TaskProcessor
from backend.domain.task import Task, TaskType
from backend.processors.ai_task_processor import ProcessTaskResult
class FakeTaskProcessor(TaskProcessor):
    
    def process_task(self, input: str) -> ProcessTaskResult:
        task = Task(
            task_id=1,
            name="Pedro",
            appliance="Antena",
            address="Calle agua",
            failure=f"FAKE: {input}",
            task_type=TaskType.NEW  
        )
        
        return ProcessTaskResult(status="ok", result=task)