from fastapi import APIRouter
from app.db.chroma_client import collection
from app.services.embedding_service import embeddings

router = APIRouter()

print("UPLOAD MODULE CARREGOU")


def clean_metadata(metadata: dict):
    cleaned = {}

    for key, value in metadata.items():
        # remove listas vazias
        if isinstance(value, list):
            if len(value) > 0:
                cleaned[key] = value

        # remove strings vazias
        elif value is not None and value != "":
            cleaned[key] = value

    return cleaned


@router.post("/upload")
def upload(data: dict):
    user_id = data["user_id"]
    content = data["content"]
    metadata = data["metadata"]

    # 🔥 limpeza obrigatória para ChromaDB
    metadata = clean_metadata(metadata)

    vector = embeddings.embed_query(content)

    collection.add(
        documents=[content],
        embeddings=[vector],
        metadatas=[metadata],
        ids=[f"{user_id}_{hash(content)}"]
    )

    return {"status": "ok"}