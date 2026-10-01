from backend.remote.task_ai import TaskAI

class FakeTaskAI(TaskAI): 

    
    def request_ai(self, text: str) -> TaskAction:
        return self.test_task