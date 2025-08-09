"use client";
import { useState } from "react";
import { parseQuestion, runCode, logInteraction } from "@/lib/api";

export default function QueryAssistant() {
  const [question, setQuestion] = useState("");
  const [resultText, setResultText] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const code = await parseQuestion(question);      // string
      const execution = await runCode(code);           // { result: [...] }

      const parsed = Array.isArray(execution?.result)
        ? execution.result.map((s: string) => {
            try { return JSON.parse(s); } catch { return s; }
          })
        : execution;

      const pretty =
        typeof parsed === "string" ? parsed : JSON.stringify(parsed, null, 2);

      setResultText(pretty); // ✅ mostramos y NO lo sobreescribimos después

      // Log en "best effort": si falla, no tocamos la UI
      try {
        await logInteraction({ question, code, result: pretty });
      } catch (e) {
        console.warn("logInteraction failed:", e);
      }
    } catch (err) {
      setResultText("Error: " + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <textarea
        className="w-full p-2 rounded border border-gray-600 bg-gray-900 text-white placeholder-gray-400"
        rows={4}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Escribe tu pregunta…"
      />
      <button
        onClick={handleSubmit}
        className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-60"
        disabled={loading}
      >
        {loading ? "Procesando…" : "Enviar"}
      </button>

      {resultText && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h2 className="font-bold mb-2 text-gray-800">Resultados:</h2>
          <pre className="whitespace-pre-wrap text-black text-sm">
            {resultText}
          </pre>
        </div>
      )}
    </div>
  );
}
