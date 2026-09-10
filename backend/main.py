from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from components.fake_task_processor import FakeTaskProcessor
from pydantic import BaseModel

app = FastAPI(title="AI Ticket Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

taskProcessor =  FakeTaskProcessor()

# Requests
class ProcessTaskRequest(BaseModel):
    text: str

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/processTask")
def process_task(request: ProcessTaskRequest) -> dict[str, str]:
    result = taskProcessor.process_task(request.text)
    return { "result": result }