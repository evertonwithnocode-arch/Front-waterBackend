import requests
import os

from app.db.chroma_client import collection
from app.services.embedding_service import embeddings
from app.services.auth_service import get_user_role

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# 🔥 DEBUG OPENROUTER EMBEDDING
def debug_embedding(question: str):
    response = requests.post(
        "https://openrouter.ai/api/v1/embeddings",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/text-embedding-3-small",
            "input": question
        }
    )

    print("\n================ RESPOSTA OPENROUTER ================")
    print("STATUS:", response.status_code)
    print("BODY:", response.text)
    print("=====================================================\n")


# 🔥 FILTER SEGURA (NUNCA RETORNA {})
def build_filter(user_id, role, entity=None, folder=None):
    base_filter = None

    # admin NÃO usa filtro por padrão
    if role != "admin":
        base_filter = {"user_id": user_id}

    # adiciona filtros extras com segurança
    if entity:
        base_filter = base_filter or {}
        base_filter["entity"] = entity

    if folder:
        base_filter = base_filter or {}
        base_filter["folder"] = folder

    return base_filter


def query_rag(question: str, user_id: str, entity: str = None, folder: str = None):
    role = get_user_role(user_id)

    filter_conditions = build_filter(user_id, role, entity, folder)

    # 🔹 1. embedding
    print("🔍 GERANDO EMBEDDING...")
    query_vector = embeddings.embed_query(question)
    print("✅ EMBEDDING OK")

    # 🔹 2. busca no banco (SAFE QUERY)
    if filter_conditions:
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=5,
            where=filter_conditions
        )
    else:
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=5
        )

    documents = results.get("documents", [[]])[0]

    # 🔥 LOG DOCUMENTOS
    print("\n================ DOCUMENTS RETORNADOS ================")
    for i, doc in enumerate(documents):
        print(f"\n--- DOC {i+1} ---")
        print(doc[:300])
    print("=====================================================\n")

    # 🔹 3. contexto
    context = "\n\n".join(documents)

    # 🔹 4. LLM (OpenRouter)
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an assistant that answers based ONLY on provided context.",
                },
                {
                    "role": "user",
                    "content": f"""
Context:
{context}

Question:
{question}
""",
                },
            ],
        },
    )

    answer = response.json()["choices"][0]["message"]["content"]

    return {
        "answer": answer,
        "documents": documents
    }