## query-assistant-service/execution-engine/app/runner.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyspark.sql import SparkSession
import traceback
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
spark = SparkSession.builder.master("local[*]").appName("ExecutionEngine").getOrCreate()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O usa ["http://localhost:3000"] si quieres restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class RunRequest(BaseModel):
    code: str
    
@app.post("/run")
def run_code(req: RunRequest):
    try:
        local_vars = {"df": spark.read.csv("/app/data.csv", header=True, inferSchema=True)}
        exec(req.code, {}, local_vars)
        result = local_vars.get("result")

        if result is None:
            return {"result": "No result variable defined"}

        # Si es DataFrame
        if hasattr(result, "toJSON"):
            return {"result": result.limit(10).toJSON().collect()}

        # Si es lista o string o lo que sea
        return {"result": result}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
