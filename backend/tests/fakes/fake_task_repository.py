from backend.repositories.task_repository import TaskRepository

class FakeTaskRepository(TaskRepository):
        

    def create(self, task: TaskAction) -> TaskAction:
        pass
            

    def get(self, task_id: int) -> TaskAction | None:
        pass
        
            
    def update(self, task: TaskAction) -> TaskAction:
        pass
            

    def list(self) -> list[TaskAction]:
        pass
        
    def searchTask(self) -> list(TaskAction):
        pass
   
    def delete(self, task_id) -> Boolean:
        pass
        
    def clear(self):
        with self.session_factory() as session:
            session.execute(delete(TaskEntity))
            session.commit()