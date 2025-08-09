import axios from "axios";

const PARSER_URL = "http://localhost:8001/parse";
const EXECUTION_URL = "http://localhost:8002/run";
const HISTORY_URL = "http://localhost:8003/history";
// const LOG_URL = "http://localhost:8004/log"; // ❌ si no existe, no lo uses

export const parseQuestion = async (question: string) => {
  const res = await axios.post(PARSER_URL, { question });
  return res.data.code; // 👈 solo el string de código
};

export const runCode = async (code: string) => {
  const res = await axios.post(EXECUTION_URL, { code });
  return res.data; // { result: [...] }
};

// "best effort": intenta loguear en history-service si tienes /log en 8003.
// Si no existe /log, puedes dejar esto como no-op.
export const logInteraction = async (payload: {
  question: string;
  code: string;
  result: string;
}) => {
  try {
    // Si tu history-service expone /log en el 8003:
    const res = await axios.post("http://localhost:8003/log", payload);
    return res.data;
  } catch {
    return { ok: false };
  }
};

export const getHistory = async () => {
  const res = await axios.get(HISTORY_URL);
  return res.data;
};
