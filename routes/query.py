# app/routes/query.py
from fastapi import APIRouter
from models.schemas import QueryInput
from services.rag_service import run_rag

router = APIRouter()

@router.post("/query")
def query(data: QueryInput):
    return run_rag(data.query, data.entity, data.workflow)