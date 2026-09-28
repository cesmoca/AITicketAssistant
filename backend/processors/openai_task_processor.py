from openai import OpenAI
from .task_processor import TaskProcessor
from ..domain.task import Task, TaskType
from ..persistence.sqlite_database import SQLiteDatabase
from ..repositories.sqlalquemy_task_repository import SQLAlchemyTaskRepository

class OpenAITaskProcessor(TaskProcessor):
    
    previous_id = None
    database = SQLiteDatabase()
    task_repository = SQLAlchemyTaskRepository(database)
    
    def __init__(self, instructions: str, model: str):
        self.model = model
        self.client = OpenAI()  
        self.instructions = instructions 
        self.database.create_tables()
        
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
        
        # Testing persistence
        # task = Task(task_id=None, name="Perico", appliance="Lavadora",address="calle faus",failure="no tira agua",task_type=TaskType.NEW)
        # self.task_repository.create(task)
        
    
        # tasks_list = self.task_repository.list()
        
        # print("Printing list")
        # print(tasks_list)
        
        # first_task = tasks_list[0]
        
        # get_task = self.task_repository.get(first_task.task_id)
        # print(get_task)
        
        # get_task.name="De los palotes"        
        # self.task_repository.update(get_task)
         
        # print("Printing list 2")
        # tasks_list = self.task_repository.list()
        # print(tasks_list)
        
        # self.task_repository.delete(get_task.task_id)
        
        # return get_task
    
    