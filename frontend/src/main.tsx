import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { useState } from "react";
import "./styles.css";

async function processTask() {
  const response = await fetch(
    "http://localhost:8000/processTask",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: "Hola!"
      })
    }
  );

  if (!response.ok) {
    throw new Error("Error procesando la tarea");
  }

  const data = await response.json();
  return data.result;
}

function App() {

  const [text, setText] = useState("");
  const [result, setResult] = useState("");

  async function handleClick() {
    const result = await processTask();
    setResult(result);
  };

  return <main>
    <h1>AI Ticket Assistant</h1>
    <p>Frontend ready.</p>
    <div>
      <h1>{text}</h1>
      <button onClick={handleClick}>Enviar Aviso</button>
      <h1>{result}</h1>
    </div>
  </main>;
}



createRoot(document.getElementById("root")!).render(
  <StrictMode><App /></StrictMode>,
);
