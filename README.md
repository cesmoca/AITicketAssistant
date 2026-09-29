# AI Ticket Assistant

AI Ticket Assistant is a full-stack learning project for turning free-form customer repair messages into structured, actionable tickets.

The project demonstrates a practical AI workflow rather than a standalone prompt demo:

1. A user submits an unstructured repair message.
2. The AI extracts a structured ticket using a typed domain model.
3. The application classifies the operation as a new ticket, update, cancellation, or undetermined request.
4. The processor applies the appropriate repository operation.
5. When an update or cancellation cannot be matched unambiguously, the API returns `resolution_required` instead of guessing.

The frontend is intentionally simple and focused on the workflow. The backend contains the domain, application processing, persistence, and AI integration layers so each responsibility can be understood and evolved independently.

## Problem it solves

Repair requests often arrive as informal conversations containing a mixture of customer identity, appliance details, address information, symptoms, corrections, and cancellation requests. Manually converting those messages into consistent operational data is slow and error-prone.

AI Ticket Assistant turns that unstructured input into a normalized ticket while preserving useful context and keeping uncertain actions safe. It is designed to demonstrate how AI extraction can be placed inside a deterministic application workflow instead of allowing a model response to directly mutate data without validation or business rules.

## Highlights

- Free-form text to structured ticket extraction.
- Structured model output with Pydantic and the OpenAI Responses API.
- Explicit operation classification: `new`, `update`, `cancel`, and `undetermined`.
- Resolution-safe behavior for ambiguous update and cancellation requests.
- Repository abstraction with a SQLAlchemy/SQLite implementation.
- React and TypeScript frontend with a responsive ticket workspace.
- Separate frontend and backend processes with CORS configured for local development.
- Unit tests using fake AI, repository, and database implementations.

## Stack

- **Frontend:** React, TypeScript, Vite, responsive CSS.
- **API:** Python, FastAPI, Pydantic, Uvicorn.
- **AI integration:** OpenAI Responses API with structured model output.
- **Persistence:** SQLAlchemy and SQLite.
- **Testing:** pytest, FastAPI `TestClient`, and hand-written fakes for external boundaries.

## Architecture

```text
React + TypeScript + Vite
              │
              │ HTTP/JSON
              ▼
FastAPI API layer
              │
              ▼
AI task processor ─── OpenAI Responses API
              │
              ▼
Task repository interface
              │
              ▼
SQLAlchemy ─── SQLite
```

### Backend layers

- `backend/main.py` exposes the FastAPI application and HTTP endpoints.
- `backend/domain/task.py` defines the `Task` domain model and task types.
- `backend/processors/ai_task_processor.py` coordinates AI extraction and business decisions.
- `backend/remote/openai_task_ai.py` adapts the OpenAI Responses API to the application’s `TaskAI` interface.
- `backend/repositories/` contains the repository contract and SQLAlchemy implementation.
- `backend/persistence/` contains SQLAlchemy entities, mapping, database setup, and SQLite configuration.
- `backend/tests/` contains unit tests and test doubles for isolated behavior testing.

### Frontend

The frontend is a Vite-powered React application written in TypeScript. It provides:

- A free-text input for incoming customer messages.
- A read-only response area for the interpreted result or a resolution request.
- A ticket list populated through the backend API.
- Refresh and clear-ticket actions.
- A responsive ticket layout that avoids horizontal scrolling while accommodating longer free-text details.

## Domain model

A ticket currently contains:

```text
task_id       integer | null
name          string  | null
appliance     string  | null
address       string  | null
failure       string  | null
other_details string  | null
task_type     new | update | cancel | undetermined
```

The AI instructions constrain extraction to information explicitly present in the customer message. Missing information is represented as `null`, while useful details that do not fit the normalized fields are preserved in `other_details`.

## API

### `POST /processTask`

Processes a free-form message.

Request:

```json
{
  "text": "Sebastian says his television only displays black and white."
}
```

Successful processing returns a typed result:

```json
{
  "status": "ok",
  "result": {
    "task_id": 1,
    "name": "Sebastian",
    "appliance": "Televisión",
    "address": null,
    "failure": "Se ve mal",
    "other_details": null,
    "task_type": "new"
  }
}
```

When an update or cancellation cannot be resolved safely:

```json
{
  "status": "resolution_required",
  "result": null
}
```

### `GET /ticketsList`

Returns the tickets currently stored in SQLite:

```json
{
  "list": []
}
```

### `DELETE /clearTickets`

Deletes the stored ticket rows while preserving the database schema.

### `GET /health`

Returns the API health status:

```json
{
  "status": "ok"
}
```

## Local setup

### Prerequisites

- Python 3.11 or newer.
- Node.js and npm.
- An OpenAI API key available as `OPENAI_API_KEY`.

### Backend

From the repository root on Windows:

```powershell
python -m venv backend\.venv
backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
backend\.venv\Scripts\python.exe -m pip install openai
$env:OPENAI_API_KEY = "your-api-key"
backend\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

On macOS or Linux:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt
backend/.venv/bin/python -m pip install openai
export OPENAI_API_KEY="your-api-key"
backend/.venv/bin/python -m uvicorn backend.main:app --reload
```

The API runs at `http://localhost:8000`. FastAPI’s interactive documentation is available at `http://localhost:8000/docs`.

Using the virtual environment’s Python executable directly is intentional: it avoids relying on shell activation scripts and makes it explicit which interpreter owns the installed dependencies.

### Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173`.

For a production-style frontend build:

```bash
npm run build
npm run preview
```

## Testing

Run the backend tests from the repository root with the project interpreter:

```powershell
backend\.venv\Scripts\python.exe -m pytest backend\tests
```

The tests use fakes for external AI and persistence dependencies, which keeps processor behavior testable without requiring a live API request or a production database.

### AI evaluation cases

The repository includes AI extraction cases in `backend/tests/utils/tickets_list.py`. They cover the four core workflow outcomes:

- `new`: create a ticket from a first-time repair request.
- `update`: recognize a correction or change to an existing request.
- `cancel`: recognize that a previously requested visit should be cancelled.
- `undetermined`: refuse to classify an ambiguous message as an actionable operation.

Run the deterministic processor tests with:

```powershell
backend\.venv\Scripts\python.exe -m pytest backend\tests\test_task_processor.py backend\tests\test_main.py
```

Run the AI extraction evaluation cases with:

```powershell
backend\.venv\Scripts\python.exe -m pytest backend\tests\test_ai_task_ai.py -s
```

The AI evaluation calls the configured OpenAI model, so it requires `OPENAI_API_KEY`, network access, and may incur API usage. The fake-based tests do not require those external resources.

## Reproducible demo

Start the backend, then send these four requests from a second terminal. The examples use PowerShell’s `Invoke-RestMethod`; the same JSON can be sent with curl or through the frontend.

```powershell
$api = "http://localhost:8000/processTask"

# 1. New ticket
Invoke-RestMethod -Method Post -Uri $api -ContentType "application/json" -Body (@{
  text = "Hola, soy Pedro Martínez. Se me ha estropeado la lavadora, no enciende. Estoy en calle Salvador número 25."
} | ConvertTo-Json)

# 2. Update existing information
Invoke-RestMethod -Method Post -Uri $api -ContentType "application/json" -Body (@{
  text = "Soy Pedro otra vez. No era la lavadora, sino la secadora la que no funciona. Vivo en calle Libertad de la Ossa."
} | ConvertTo-Json)

# 3. Cancellation
Invoke-RestMethod -Method Post -Uri $api -ContentType "application/json" -Body (@{
  text = "Soy Pedro otra vez. Ya no vengas, que nos hemos apañado."
} | ConvertTo-Json)

# 4. Undetermined request
Invoke-RestMethod -Method Post -Uri $api -ContentType "application/json" -Body (@{
  text = "Llevo tres días esperando, pásate hombre, que la mujer se va a cabrear."
} | ConvertTo-Json)
```

Expected high-level outcomes:

| Case | Expected `task_type` / status | Behavior |
| --- | --- | --- |
| New ticket | `new` / `ok` | Extract and persist a new task. |
| Update | `update` / `ok` or `resolution_required` | Update only when the existing ticket match is unambiguous. |
| Cancellation | `cancel` / `ok` or `resolution_required` | Delete only when the target ticket match is unambiguous. |
| Ambiguous message | `undetermined` / `ok` | Preserve the extracted information without inventing an operation. |

The exact result of update and cancellation depends on the current contents of the local SQLite database. If more than one candidate matches, the safe result is `resolution_required`.

## Design decisions worth reviewing

### Structured AI output

The AI adapter requests a parsed `Task` rather than relying on fragile string parsing. This makes the boundary between probabilistic extraction and deterministic application logic explicit.

### Safe ambiguity handling

An update or cancellation may match zero or multiple existing tickets. In those cases, the processor returns `resolution_required` and does not silently modify or delete data. This is a deliberate safety boundary for an operational workflow.

### Repository boundary

The processor depends on repository behavior rather than directly manipulating SQLAlchemy sessions. This keeps business decisions independent from SQLite and makes unit testing with fakes straightforward.

### Local-first development

The project currently uses SQLite and two local development servers. This keeps setup small while preserving seams where a production database, authentication, background jobs, or deployment-specific configuration could be introduced later.

## Current scope and next steps

This is a focused portfolio and learning project, not a production deployment. Natural next steps include:

- Add stronger runtime validation for external API responses.
- Move the OpenAI dependency into the backend requirements file.
- Add consistent API error responses and frontend error feedback.
- Add database migrations and a production database adapter.
- Add authentication, authorization, and audit logging.
- Add integration tests for the HTTP endpoints.
- Add explicit timestamps if ticket ordering by date is required.
- Add confirmation and authorization safeguards around bulk deletion.

## Technical retrospective

### What I learned

- A useful AI feature needs a strong typed boundary between model output and application behavior.
- The difficult part is not extracting fields; it is deciding what the application is allowed to do when the input is incomplete or ambiguous.
- Repository interfaces and fakes make the business processor easier to test without depending on SQLite or a live model.

### Decisions I made

- I used structured Pydantic output instead of parsing free-form model text.
- I separated extraction, processing, persistence, and HTTP concerns into different layers.
- I introduced `resolution_required` as an explicit safety state so updates and cancellations do not guess.
- I kept SQLite and local development servers to minimize setup while the domain and workflow are still evolving.

### What I would do differently next

- Add a dedicated evaluation runner with stable fixtures, recorded model outputs, and field-level scoring.
- Validate and version the AI contract at runtime rather than trusting external JSON implicitly.
- Add timestamps and explicit ticket history before implementing production ordering or audit requirements.
- Move configuration and secrets into a settings layer, add migrations, and replace bulk deletion with an authenticated, confirmed operation.

## License

No license has been defined yet.
