from fastapi import APIRouter
from app.db.chroma_client import collection
from app.services.embedding_service import embeddings

router = APIRouter()

@router.post("/upload")
def upload(data: dict):
    user_id = data["user_id"]
    content = data["content"]
    metadata = data["metadata"]

    vector = embeddings.embed_query(content)

    collection.add(
        documents=[content],
        embeddings=[vector],
        metadatas=[metadata],
        ids=[f"{user_id}_{hash(content)}"]
    )

    return {"status": "ok"}