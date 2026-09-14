from openai import OpenAI
from .task_processor import TaskProcessor
from .task import Task
class OpenAITaskProcessor(TaskProcessor):
    
    previous_id = None
    
    def __init__(self, instructions: str, model: str):
        self.model = model
        self.client = OpenAI()  
        self.instructions = instructions 
        
    def process_task(self, text: str) -> Task:

        response = self.client.responses.parse(
            model=self.model,
            input=text,
            instructions=self.instructions,
            #previous_response_id=self.previous_id,
            text_format=Task
        )

        self.previous_id = response.id
        
        return response.output_parsed
    
    