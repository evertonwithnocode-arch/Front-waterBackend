import requests
import os

from app.db.chroma_client import collection
from app.services.embedding_service import embeddings
from app.services.auth_service import get_user_role

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def build_filter(user_id, role, entity=None, folder=None):
    if role == "admin":
        base_filter = {}
    else:
        base_filter = {"user_id": user_id}

    if entity:
        base_filter["entity"] = entity

    if folder:
        base_filter["folder"] = folder

    return base_filter


def query_rag(question: str, user_id: str, entity: str = None, folder: str = None):
    role = get_user_role(user_id)

    filter_conditions = build_filter(user_id, role, entity, folder)

    # 🔹 1. embedding
    query_vector = embeddings.embed_query(question)

    # 🔹 2. busca no banco
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=5,
        where=filter_conditions
    )

    documents = results.get("documents", [[]])[0]

      # 🔥 COLOCA O LOG AQUI 👇
    print("\n================ DOCUMENTS RETORNADOS ================")
    for i, doc in enumerate(documents):
        print(f"\n--- DOC {i+1} ---")
        print(doc[:300])  # primeiros 300 chars
    print("=====================================================\n")

    # 🔹 3. monta contexto
    context = "\n\n".join(documents)

    # 🔹 4. chama OpenRouter (LLM)
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-4o-mini",  # ou outro
            "messages": [
                {
                    "role": "system",
                    "content": "You are an assistant that answers based ONLY on provided context."
                },
                {
                    "role": "user",
                    "content": f"""
Context:
{context}

Question:
{question}
"""
                }
            ]
        }
    )

    answer = response.json()["choices"][0]["message"]["content"]

    return {
        "answer": answer,
        "documents": documents  # opcional (debug ou citations)
    }