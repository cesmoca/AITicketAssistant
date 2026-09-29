from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .remote.openai_task_ai import OpenAITaskAI
from .repositories.sqlalquemy_task_repository import SQLAlchemyTaskRepository
from .persistence.sqlite_database import SQLiteDatabase
from .processors.ai_task_processor import AITaskProcessor 
from .domain.task import Task, TaskType
from .constants import SYSTEM_PROMPT

# Frontend: cd frontend && npm run dev
# Backend: uvicorn backend.main:app --reload (desde directorio root)

app = FastAPI(title="AI Ticket Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = SQLiteDatabase()
repository = SQLAlchemyTaskRepository(session_factory=database.SessionLocal)
task_ai = OpenAITaskAI(database=database, model="gpt-5.6-luna", instructions=SYSTEM_PROMPT)

app.task_processor =  AITaskProcessor(repository, task_ai)

class ProcessTaskRequest(BaseModel):
    text: str
    
# Requests
@app.post("/processTask")
def process_task(request: ProcessTaskRequest) -> dict[str, Task]:
    task = app.task_processor.process_task(request.text)
    print(task)
    return { "result": task }

@app.get("/ticketsList")
def health() -> dict[str, list[Task]]:
    tickets_list = repository.list()
    return {"list": tickets_list}

@app.delete("/clearTickets")
def clear_tickets() -> dict[str, str]:
    repository.clear()
    return {"status": "ok"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}