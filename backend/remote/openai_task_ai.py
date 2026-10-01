from openai import OpenAI
from ..remote.task_ai import TaskAI
from ..domain.task_action import TaskAction, TaskActionType
class OpenAITaskAI(TaskAI):
    
    previous_id = None
    
    def __init__(self, instructions: str, model: str):
        self.model = model
        self.client = OpenAI()  
        self.instructions = instructions 
        
    def request_ai(self, text: str) -> TaskAction:

        response = self.client.responses.parse(
            model=self.model,
            input=text,
            instructions=self.instructions,
            #previous_response_id=self.previous_id,
            text_format=TaskAction
        )

        self.previous_id = response.id

        return response.output_parsed