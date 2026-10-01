from backend.processors.task_processor import TaskProcessor
from backend.domain.task_action import TaskAction, TaskActionType
from backend.processors.ai_task_processor import ProcessTaskResult
class FakeTaskProcessor(TaskProcessor):
    
    def process_task(self, input: str) -> ProcessTaskResult:
        task = TaskAction(
            task_id=1,
            name="Pedro",
            appliance="Antena",
            address="Calle agua",
            failure=f"FAKE: {input}",
            other_details="Tiene prisa",            
            task_type=TaskActionType.NEW
        )
        
        return ProcessTaskResult(status="ok", result=task)