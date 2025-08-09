## query-assistant-service/api-gateway/app/main.py
from fastapi import FastAPI, HTTPException
from app.routes.query import router as query_router

app = FastAPI(title="Query Assistant API")
app.include_router(query_router)