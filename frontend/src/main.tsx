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

const tickets = [
  {
    date: "2026-09-29",
    name: "María López",
    appliance: "Washing machine",
    address: "Calle Mayor 12",
    failure: "Does not start",
    status: "Pending",
    statusClass: "status-badge"
  },
  {
    date: "2026-09-28",
    name: "Carlos García",
    appliance: "Oven",
    address: "Avenida del Sol 8",
    failure: "Not heating",
    status: "In progress",
    statusClass: "status-badge status-badge--muted"
  },
  {
    date: "2026-09-27",
    name: "Ana Martín",
    appliance: "Refrigerator",
    address: "Plaza España 4",
    failure: "Leaking water",
    status: "Completed",
    statusClass: "status-badge status-badge--muted"
  }
];

function App() {

  const [text, setText] = useState("");
  const [result, setResult] = useState("");

  async function handleClick() {
    const result = await processTask(text);
    setResult(JSON.stringify(result));
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
        <button className="primary-button" onClick={handleClick} type="button">Send</button>
      </div>
    </section>

    <section className="panel ticket-panel" aria-labelledby="tickets-title">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Ticket queue</p>
          <h2 id="tickets-title">Tickets</h2>
        </div>
        <button className="secondary-button" type="button">Refresh</button>
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
        {[...tickets]
          .sort((first, second) => second.date.localeCompare(first.date))
          .map((ticket) => (
            <div className="ticket-row" role="row" key={`${ticket.date}-${ticket.name}`}>
              <span role="cell" data-label="Date">{ticket.date.split("-").reverse().join("/")}</span>
              <span role="cell" data-label="Name">{ticket.name}</span>
              <span role="cell" data-label="Appliance">{ticket.appliance}</span>
              <span role="cell" data-label="Address">{ticket.address}</span>
              <span role="cell" data-label="Failure">{ticket.failure}</span>
              <span role="cell" data-label="Status"><span className={ticket.statusClass}>{ticket.status}</span></span>
            </div>
          ))}
      </div>
    </section>
  </main>;
}



createRoot(document.getElementById("root")!).render(
  <StrictMode><App /></StrictMode>,
);
