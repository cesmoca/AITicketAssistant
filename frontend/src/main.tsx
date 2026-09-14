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

function App() {

  const [text, setText] = useState("");
  const [result, setResult] = useState("");

  async function handleClick() {
    const result = await processTask(text);
    setResult(result);
  };

  return <main>
    <h1>AI Ticket Assistant</h1>
    <p>Frontend ready.</p>
    <div>
      <button onClick={handleClick}>Enviar Aviso</button>
      <p></p>
      <h4>Envio</h4>
      <textarea
      value={text}
      onChange={(event) => setText(event.target.value)}
      />
      <h4>Respuesta</h4>

      <textarea
      value={result}
      contentEditable="false"
      />
    </div>
  </main>;
}



createRoot(document.getElementById("root")!).render(
  <StrictMode><App /></StrictMode>,
);
