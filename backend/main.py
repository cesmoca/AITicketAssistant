from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .remote.openai_task_ai import OpenAITaskAI
from .repositories.sqlalquemy_task_repository import SQLAlchemyTaskRepository
from .persistence.sqlite_database import SQLiteDatabase
from .processors.ai_task_processor import AITaskProcessor, ProcessTaskRequest, ProcessTaskResult
from .domain.task_action import TaskAction, TaskActionType
from .constants import SYSTEM_PROMPT, MODEL

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
database.create_tables()
repository = SQLAlchemyTaskRepository(session_factory=database.SessionLocal)
task_ai = OpenAITaskAI(model=MODEL, instructions=SYSTEM_PROMPT)

app.task_processor =  AITaskProcessor(repository, task_ai)

# Requests
@app.post("/processTask")
def process_task(request: ProcessTaskRequest) -> ProcessTaskResult:
    result = app.task_processor.process_task(request.text)
    return result

@app.get("/ticketsList")
def health() -> dict[str, list[TaskAction]]:
    tickets_list = repository.list()
    return {"list": tickets_list}

@app.delete("/clearTickets")
def clear_tickets() -> dict[str, str]:
    repository.clear()
    return {"status": "ok"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}