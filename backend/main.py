from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .components.fake_task_processor import FakeTaskProcessor
from .components.openai_task_processor import OpenAITaskProcessor
from pydantic import BaseModel

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

instructions = ("Haz como si fueras un asistente para un reparador"
               "de electrodomesticos y necesitas sacar la informacion"
               "clave de los avisos de reparacion a partir de la"
               "llamada de un cliente"
)

#taskProcessor =  FakeTaskProcessor()
taskProcessor =  OpenAITaskProcessor(model="gpt-5.6-luna", instructions=instructions)

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