from app.db.chroma_client import collection
from app.services.embedding_service import embeddings
from app.services.auth_service import get_user_role


def build_filter(user_id, role, entity=None, folder=None):
    """
    Novo modelo simplificado:
    - admin vê tudo
    - outros usuários: apenas seus próprios docs (ou filtrados)
    """

    # 🔥 admin vê tudo
    if role == "admin":
        base_filter = {}
    else:
        base_filter = {"user_id": user_id}

    # 🔹 filtros opcionais (vertical / folder)
    if entity:
        base_filter["entity"] = entity

    if folder:
        base_filter["folder"] = folder

    return base_filter


def query_rag(question: str, user_id: str, entity: str = None, folder: str = None):
    role = get_user_role(user_id)

    filter_conditions = build_filter(user_id, role, entity, folder)

    # 🔥 gerar emsdbedding
    query_vector = embeddings.embed_query(question)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=5,
        where=filter_conditions
    )

    return results