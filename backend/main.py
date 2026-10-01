from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .remote.openai_ticket_ai import OpenAITicketAI
from .repositories.sqlalquemy_ticket_repository import SQLAlchemyTicketRepository
from .persistence.sqlite_database import SQLiteDatabase
from .processors.ai_ticket_processor import AITicketProcessor, ProcessTicketRequest, ProcessTicketResult
from .domain.ticket_action import TicketAction, TicketActionType
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
repository = SQLAlchemyTicketRepository(session_factory=database.SessionLocal)
ticket_ai = OpenAITicketAI(model=MODEL, instructions=SYSTEM_PROMPT)

app.ticket_processor =  AITicketProcessor(repository, ticket_ai)

# Requests
@app.post("/processTicket")
def process_ticket(request: ProcessTicketRequest) -> ProcessTicketResult:
    result = app.ticket_processor.process_ticket(request.text)
    return result

@app.get("/ticketsList")
def health() -> dict[str, list[TicketAction]]:
    tickets_list = repository.list()
    return {"list": tickets_list}

@app.delete("/clearTickets")
def clear_tickets() -> dict[str, str]:
    repository.clear()
    return {"status": "ok"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}