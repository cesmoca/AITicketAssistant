from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .processors.openai_task_processor import OpenAITaskProcessor
from .domain.task import Task
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

taskProcessor =  OpenAITaskProcessor(model="gpt-5.6-luna", instructions=SYSTEM_PROMPT)

# Requests
class ProcessTaskRequest(BaseModel):
    text: str

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/processTask")
def process_task(request: ProcessTaskRequest) -> dict[str, Task]:
    result = taskProcessor.process_task(request.text)
    print(result)
    return { "result": result }