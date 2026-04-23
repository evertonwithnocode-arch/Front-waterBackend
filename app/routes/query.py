from fastapi import APIRouter, HTTPException
from app.services.rag_service import query_rag
from app.db.chroma_client import collection

router = APIRouter()

print("QUERY MODULE CARREGOU")


@router.post("/query")
def query(data: dict):
    return query_rag(
        question=data["question"],
        user_id=data["user_id"],
        entity=data.get("entity"),
        folder=data.get("folder")
    )


# 🔥 DEBUG TEMPORÁRIO
@router.get("/debug-docs")
def debug_docs():
    try:
        results = collection.get()

        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])
        ids = results.get("ids", [])

        debug_list = []

        for i in range(len(documents)):
            metadata = metadatas[i] if i < len(metadatas) else {}

            debug_list.append({
                "id": ids[i] if i < len(ids) else None,
                "preview": documents[i][:200] if documents[i] else None,
                "document_name": metadata.get("document_name"),
                "entity": metadata.get("entity"),
                "folder": metadata.get("folder"),
                "user_id": metadata.get("user_id")
            })

        return {
            "total_documents": len(documents),
            "documents": debug_list
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))