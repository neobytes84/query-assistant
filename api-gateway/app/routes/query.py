## query-assistant-service/api-gateway/app/routes/query.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os

router = APIRouter()

QUERY_PARSER_URL = os.getenv("QUERY_PARSER_URL", "http://query-parser:8001")
EXECUTION_ENGINE_URL = os.getenv("EXECUTION_ENGINE_URL", "http://execution-engine:8002")
HISTORY_SERVICE_URL = os.getenv("HISTORY_SERVICE_URL", "http://history-service:8003")

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def process_query(request: QueryRequest):
    try:
        async with httpx.AsyncClient() as client:
            parser_response = await client.post(f"{QUERY_PARSER_URL}/parse", json={"question": request.question})
            parser_response.raise_for_status()
            spark_code = parser_response.json()["code"]
            
            exec_response = await client.post(f"{EXECUTION_ENGINE_URL}/run", json={"code": spark_code})
            exec_response.raise_for_status()
            result = exec_response.json()["result"]
            
            await client.post(f"{HISTORY_SERVICE_URL}/log", json={
                "question": request.question,
                "code": spark_code,
                "result": result
            })
    
            return {"result": result}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
                                 