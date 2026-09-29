from backend.repositories.task_repository import TaskRepository

class FakeTaskRepository(TaskRepository):
        

    def create(self, task: Task) -> Task:
        pass
            

    def get(self, task_id: int) -> Task | None:
        pass
        
            
    def update(self, task: Task) -> Task:
        pass
            

    def list(self) -> list[Task]:
        pass
        
    def searchTask(self) -> list(Task):
        pass
   
    def delete(self, task_id) -> Boolean:
        pass
        
    def clear(self):
        with self.session_factory() as session:
            session.execute(delete(TaskEntity))
            session.commit()