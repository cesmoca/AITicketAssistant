from .task_processor import TaskProcessor
from openai import OpenAI

class OpenAITaskProcessor(TaskProcessor):
    
    previous_id = None
    
    def __init__(self, instructions: str, model: str):
        self.model = model
        self.client = OpenAI()  
        self.instructions = instructions 
        
    def process_task(self, text: str) -> str:

        response = self.client.responses.create(
            model=self.model,
            input=text,
            instructions=self.instructions,
            previous_response_id=self.previous_id
        )

        self.previous_id = response.id
        
        return response.output_text 
    
    