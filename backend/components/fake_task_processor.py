from .task_processor import TaskProcessor

class FakeTaskProcessor(TaskProcessor):
    def process_task(self, input: str) -> str:
        result = input
        return f"FAKE: {input}"