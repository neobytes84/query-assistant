## query-assistant-service/query-parser/app/parser.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import openai
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O usa ["http://localhost:3000"] si quieres restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ParseRequest(BaseModel):
    question: str
    

@app.post("/parse")
def parse_question(req: ParseRequest):
    question = req.question.lower()

    if "cnt" in question:
        return {"code": 'result = df.select("cnt").limit(5)'}
    elif "season" in question:
        return {"code": 'result = df.select("season").limit(5)'}
    else:
        return {"code": 'result = df.limit(5)'}
