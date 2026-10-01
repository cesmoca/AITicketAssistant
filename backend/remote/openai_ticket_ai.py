from openai import OpenAI

from ..domain.ticket_action import TicketAction
from ..processors.ticket_processor import ProcessTicketRequest
from ..remote.ticket_ai import TicketAI


class OpenAITicketAI(TicketAI):
    
    previous_id = None
    
    def __init__(self, instructions: str, model: str):
        self.model = model
        self.client = OpenAI()  
        self.instructions = instructions 
        
    def request_ai(self, request: ProcessTicketRequest) -> TicketAction:

        response = self.client.responses.parse(
            model=self.model,
            input=request.text,
            instructions=self.instructions,
            #previous_response_id=self.previous_id,
            text_format=TicketAction
        )

        self.previous_id = response.id

        return response.output_parsed