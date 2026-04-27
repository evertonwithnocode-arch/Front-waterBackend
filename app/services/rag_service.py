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
    import json
    import time

    request_id = str(time.time())

    print("\n================ RAG DEBUG START =================")
    print(f"🆔 request_id: {request_id}")
    print(f"❓ question: {question}")
    print(f"👤 user_id: {user_id}")
    print(f"🏷️ entity: {entity}")
    print(f"📁 folder: {folder}")

    role = get_user_role(user_id)
    print(f"🔐 role: {role}")

    filter_conditions = build_filter(user_id, role, entity, folder)
    print(f"🔎 filter_conditions: {filter_conditions}")

    # 🔹 1. embedding
    print("\n🔍 GERANDO EMBEDDING...")
    query_vector = embeddings.embed_query(question)
    print("✅ EMBEDDING OK")

    # 🔹 2. busca
    print("\n📡 CONSULTANDO CHROMA...")
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
    metadatas = results.get("metadatas", [[]])[0]
    sources = [
    {
        "document_name": m.get("document_name"),
        "file_name": m.get("file_name"),
        "entity": m.get("entity"),
        "folder": m.get("folder"),
    }
    for m in metadatas
]
    distances = results.get("distances", [[]])[0]

    print(f"\n📊 RESULTADOS BRUTOS:")
    print(f"docs: {len(documents)} | metadatas: {len(metadatas)} | distances: {len(distances)}")

    # 🔥 DEBUG COMPLETO POR DOCUMENTO
    print("\n================ DOCUMENTOS RETORNADOS ================")
    for i in range(len(documents)):
        metadata = metadatas[i] if i < len(metadatas) else {}
        score = distances[i] if i < len(distances) else None

        print(f"\n--- DOC {i+1} ---")
        print(f"📄 preview: {documents[i][:200]}")
        print(f"📁 metadata: {metadata}")
        print(f"📊 score: {score}")

        # 👇 aqui você vê o nome do documento se existir
        print(f"📛 document_name: {metadata.get('document_name')}")
        print(f"🏷️ entity: {metadata.get('entity')}")
        print(f"📂 folder: {metadata.get('folder')}")

    print("=====================================================\n")

    # 🔹 3. contexto
    context = "\n\n".join(documents)

    # 🔹 4. LLM
    print("🤖 CHAMANDO LLM...")
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
                    "content": "You are an assistant that answers based ONLY on provided context. If the answer is not in the context, say you don't know.",
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

    print("\n================ OPENROUTER RESPONSE ================")
    print("STATUS:", response.status_code)
    print("BODY:", response.text)
    print("=====================================================\n")

    data = response.json()

    if "choices" not in data:
        print("❌ ERRO NA RESPOSTA DO OPENROUTER:", data)
        raise Exception(f"Erro OpenRouter: {data}")

    answer = data["choices"][0]["message"]["content"]

    return {
    "answer": answer,
    "documents": documents,
    "sources": sources
    }