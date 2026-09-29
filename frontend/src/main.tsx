import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { useState } from "react";
import "./styles.css";

async function processTask(text: String) {
  const response = await fetch(
    "http://localhost:8000/processTask",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: text
      })
    }
  );

  if (!response.ok) {
    throw new Error("Error procesando la tarea");
  }

  const data = await response.json();
  return data.result;
}

async function listTickets(): Promise<Ticket[]> {
  const response = await fetch(
    "http://localhost:8000/ticketsList",
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      },
    }
  );

  if (!response.ok) {
    throw new Error("Error obteniendo los tickets");
  }

  const data: { list: Ticket[] } = await response.json();
  return data.list;
}

interface Ticket {
  task_id: number | null;
  name: string | null;
  appliance: string | null;
  address: string | null;
  failure: string | null;
  task_type: string;
}

function App() {

  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [ticketsList, setTicketsList] = useState<Ticket[]>([]);

  async function handleSendClick() {
    const result = await processTask(text);
    setResult(JSON.stringify(result));
  };

  async function handleRefreshClick() {
    const tickets = await listTickets();
    setTicketsList(tickets);
  };

  return <main>
    <header className="page-header">
      <div>
        <p className="eyebrow">Workspace</p>
        <h1>AI Ticket Assistant</h1>
        <p className="subtitle">Review and process support tasks from one place.</p>
      </div>
    </header>

    <section className="panel compose-panel" aria-labelledby="ticket-input-title">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Ticket workspace</p>
          <h2 id="ticket-input-title">Ticket input</h2>
        </div>
      </div>

      <div className="editor-grid">
        <label>
          <span>Free text</span>
          <textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Write or paste the ticket information here..."
          />
        </label>
        <label>
          <span>Understanding and changes</span>
          <textarea
            value={result}
            readOnly
            aria-readonly="true"
            placeholder="The understood information and applied changes will appear here..."
          />
        </label>
      </div>
      <div className="action-row">
        <button className="primary-button" onClick={handleSendClick} type="button">Send</button>
      </div>
    </section>

    <section className="panel ticket-panel" aria-labelledby="tickets-title">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Ticket queue</p>
          <h2 id="tickets-title">Tickets</h2>
        </div>
        <button className="secondary-button" onClick={handleRefreshClick} type="button">Refresh</button>
      </div>

      <div className="ticket-table" role="table" aria-label="Ticket rows">
        <div className="ticket-row ticket-header" role="row">
          <span role="columnheader">Date</span>
          <span role="columnheader">Name</span>
          <span role="columnheader">Appliance</span>
          <span role="columnheader">Address</span>
          <span role="columnheader">Failure</span>
          <span role="columnheader">Status</span>
        </div>
        {ticketsList.map((ticket) => (
            <div className="ticket-row" role="row" key={ticket.task_id ?? `${ticket.name}-${ticket.appliance}`}>
              <span role="cell" data-label="Date">—</span>
              <span role="cell" data-label="Name">{ticket.name ?? "—"}</span>
              <span role="cell" data-label="Appliance">{ticket.appliance ?? "—"}</span>
              <span role="cell" data-label="Address">{ticket.address ?? "—"}</span>
              <span role="cell" data-label="Failure">{ticket.failure ?? "—"}</span>
              <span role="cell" data-label="Status">
                <span className="status-badge status-badge--muted">{ticket.task_type}</span>
              </span>
            </div>
          ))}
      </div>
    </section>
  </main>;
}



createRoot(document.getElementById("root")!).render(
  <StrictMode><App /></StrictMode>,
);
