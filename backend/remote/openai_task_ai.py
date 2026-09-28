from openai import OpenAI
from ..remote.task_ai import TaskAI
from ..domain.task import Task, TaskType
from ..persistence.sqlite_database import SQLiteDatabase
from ..repositories.sqlalquemy_task_repository import SQLAlchemyTaskRepository

class OpenAITaskAI(TaskAI):
    
    previous_id = None
    
    def __init__(self, database, instructions: str, model: str):
        self.model = model
        self.client = OpenAI()  
        self.instructions = instructions 
        self.database = database
        self.task_repository = SQLAlchemyTaskRepository(database.SessionLocal)
        self.database.create_tables()
        
    def request_ai(self, text: str) -> Task:

        response = self.client.responses.parse(
            model=self.model,
            input=text,
            instructions=self.instructions,
            #previous_response_id=self.previous_id,
            text_format=Task
        )

        self.previous_id = response.id

        return response.output_parsed