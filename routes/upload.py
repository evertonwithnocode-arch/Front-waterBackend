# app/routes/upload.py
from fastapi import APIRouter
from models.schemas import DocumentInput
from services.embedding_service import process_document

router = APIRouter()

@router.post("/upload")
def upload(doc: DocumentInput):
    return process_document(doc.content, doc.metadata)