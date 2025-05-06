# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from .db import engine
from .utils import is_select_query, validate_syntax

app = FastAPI()

class QueryRequest(BaseModel):
    sql: str

@app.post("/query")
def run_query(req: QueryRequest):
    sql = req.sql

    # ─── Requirement 1: Must start with SELECT ─────────────────────────
    if not is_select_query(sql):
        raise HTTPException(
            status_code=400,
            detail="Only SELECT statements are allowed, and no forbidden keywords."
        )

    # ─── Requirement 3: Syntax validation ───────────────────────────────
    if not validate_syntax(sql):
        raise HTTPException(status_code=400, detail="Malformed or invalid SQL syntax.")

    # ─── Execute safely ────────────────────────────────────────────────
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = [dict(row) for row in result.mappings()]
        return {"rows": rows}

    except ProgrammingError:
        # Catches psycopg2 syntax errors and other SQL execution errors
        raise HTTPException(status_code=400, detail="Malformed or invalid SQL syntax.")
    except Exception as e:
        # Any other unexpected errors → 500
        raise HTTPException(status_code=500, detail=f"Execution error: {e}")

