# history-service/app/db.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # No pongas credenciales reales como default.
    raise RuntimeError("DATABASE_URL no está definido (usa .env o variables de entorno)")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class QueryLog(Base):
    __tablename__ = "query_logs"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    code = Column(Text)
    result = Column(Text)

Base.metadata.create_all(bind=engine)

class LogRequest(BaseModel):
    question: str
    code: str
    result: str

@app.post("/log")
async def log_interaction(log: LogRequest):
    try:
        db = SessionLocal()
        item = QueryLog(question=log.question, code=log.code, result=log.result)
        db.add(item)
        db.commit()
        db.refresh(item)
        db.close()
        return {"message": "Logged successfully", "id": item.id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/history")
def get_history():
    try:
        db = SessionLocal()
        items = db.query(QueryLog).all()
        db.close()
        return {"history": [
            {"id": x.id, "question": x.question, "code": x.code, "result": x.result}
            for x in items
        ]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
