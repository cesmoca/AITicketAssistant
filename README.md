# AI Ticket Assistant

Minimal React + TypeScript frontend and FastAPI backend.

## Run the backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API is available at `http://localhost:8000`; health check: `GET /health`.

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend is available at `http://localhost:5173`.
