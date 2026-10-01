from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .constants import MODEL, SYSTEM_PROMPT
from .domain.ticket import Ticket
from .persistence.sqlite_database import SQLiteDatabase
from .processors.ai_ticket_processor import (
    AITicketProcessor,
    ProcessTicketRequest,
    ProcessTicketResult,
)
from .remote.openai_ticket_ai import OpenAITicketAI
from .repositories.sqlalquemy_ticket_repository import SQLAlchemyTicketRepository

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
repository = SQLAlchemyTicketRepository(session_factory=database.SessionLocal)
ticket_ai = OpenAITicketAI(model=MODEL, instructions=SYSTEM_PROMPT)

app.ticket_processor =  AITicketProcessor(repository, ticket_ai)

# Requests
@app.post("/processTicket")
def process_ticket(request: ProcessTicketRequest) -> ProcessTicketResult:
    result = app.ticket_processor.process_ticket(request)
    return result

@app.get("/listTickets")
def list_tickets() -> dict[str, list[Ticket]]:
    tickets_list = repository.list()
    return {"list": tickets_list}

@app.delete("/clearTickets")
def clear_tickets() -> dict[str, str]:
    repository.clear()
    return {"status": "ok"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}