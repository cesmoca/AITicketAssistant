import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function App() {
  return <main><h1>AI Ticket Assistant</h1><p>Frontend ready.</p></main>;
}

createRoot(document.getElementById("root")!).render(
  <StrictMode><App /></StrictMode>,
);
