import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { useState } from "react";
import "./styles.css";

interface TaskInfo {
  name: string | null;
  appliance: string | null;
  address: string | null;
  failure: string | null;
  other_details: string | null;
}

interface Ticket {
  id: number;
  status: "active" | "completed" | "cancelled" | "suspended" | "other";
  info: TaskInfo;
}

interface ProcessTicketResult {
  status: string;
  data: string | null;
  result: Ticket | null;
}

async function processTicket(text: string): Promise<ProcessTicketResult> {
  const response = await fetch(
    "http://localhost:8000/processTicket",
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

  const data: ProcessTicketResult = await response.json();
  return data;
}

async function listTickets(): Promise<Ticket[]> {
  const response = await fetch(
    "http://localhost:8000/listTickets",
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

function App() {

  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [ticketsList, setTicketsList] = useState<Ticket[]>([]);

  async function handleSendClick() {
    try {
      const response = await processTicket(text);
      setResult(JSON.stringify(response, null, 2));
    } catch (error) {
      setResult(error instanceof Error ? error.message : "Error procesando la tarea");
    }
  };

  async function handleRefreshClick() {
    const tickets = await listTickets();
    setTicketsList(tickets);
  };

  async function handleClearDatabaseClick() {
    const response = await fetch("http://localhost:8000/clearTickets", {
      method: "DELETE"
    });

    if (!response.ok) {
      throw new Error("Error borrando los tickets");
    }

    setTicketsList([]);
  }

  return <main>
    <header className="page-header">
      <div>
        <p className="eyebrow">Workspace</p>
        <h1>AI Ticket Assistant</h1>
        <p className="subtitle">Review and process support tickets from one place.</p>
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
        <div className="ticket-actions">
          <button className="danger-button" onClick={handleClearDatabaseClick} type="button">Clear database</button>
          <button className="secondary-button" onClick={handleRefreshClick} type="button">Refresh</button>
        </div>
      </div>

      <div className="ticket-table" role="table" aria-label="Ticket rows">
        <div className="ticket-row ticket-header" role="row">
          <span role="columnheader">Date</span>
          <span role="columnheader">Name</span>
          <span role="columnheader">Appliance</span>
          <span role="columnheader">Address</span>
          <span role="columnheader">Failure</span>
          <span role="columnheader">Other Details</span>
          <span role="columnheader">Status</span>
        </div>
        {ticketsList.map((ticket) => (
            <div className="ticket-row" role="row" key={ticket.id}>
              <span role="cell" data-label="Date">&mdash;</span>
              <span role="cell" data-label="Name">{ticket.info.name ?? "\u2014"}</span>
              <span role="cell" data-label="Appliance">{ticket.info.appliance ?? "\u2014"}</span>
              <span role="cell" data-label="Address">{ticket.info.address ?? "\u2014"}</span>
              <span role="cell" data-label="Failure">{ticket.info.failure ?? "\u2014"}</span>
              <span role="cell" data-label="Other Details">{ticket.info.other_details ?? "\u2014"}</span>
              <span role="cell" data-label="Status">
                <span className="status-badge status-badge--muted">{ticket.status}</span>
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
