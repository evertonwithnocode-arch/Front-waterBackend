from app.db.chroma_client import collection
from app.services.embedding_service import embeddings
from app.services.auth_service import get_user_role

def build_filter(user_id, role):
    
    if role == "admin":
        return {}

    if role == "technical":
        return {"entity": "XPC"}

    if role == "commercial":
        return {"entity": "Frontwater"}

    if role == "client":
        return {"evidence_level": "approved"}

    return {}

def query_rag(question: str, user_id: str):
    role = get_user_role(user_id)

    filter_conditions = build_filter(user_id, role)

    query_vector = embeddings.embed_query(question)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=5,
        where=filter_conditions
    )

    return results