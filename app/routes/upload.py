import logging
from fastapi import APIRouter, HTTPException
from app.db.chroma_client import collection
from app.services.embedding_service import embeddings

router = APIRouter()

# 🔥 configuração básica de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("🚀 UPLOAD MODULE CARREGADO")


def clean_metadata(metadata: dict):
    cleaned = {}

    for key, value in metadata.items():
        if isinstance(value, list):
            if len(value) > 0:
                cleaned[key] = value
        elif value is not None and value != "":
            cleaned[key] = value

    return cleaned


@router.post("/upload")
def upload(data: dict):
    try:
        logger.info("📥 [UPLOAD] Requisição recebida")

        # 🔹 validação básica
        user_id = data.get("user_id")
        content = data.get("content")
        metadata = data.get("metadata")

        if not user_id or not content or not metadata:
            logger.error("❌ Payload inválido")
            raise HTTPException(status_code=400, detail="Invalid payload")

        logger.info(f"👤 user_id: {user_id}")
        logger.info(f"📄 content size: {len(content)} chars")
        logger.info(f"🧾 metadata recebido: {metadata}")

        # 🔹 limpeza
        metadata = clean_metadata(metadata)
        logger.info(f"🧹 metadata limpo: {metadata}")

        # 🔹 gerar embedding
        logger.info("🧠 Gerando embedding...")
        vector = embeddings.embed_query(content)
        logger.info(f"✅ Embedding gerado (dim={len(vector)})")

        # 🔹 salvar no Chroma
        doc_id = f"{user_id}_{hash(content)}"
        logger.info(f"💾 Salvando no ChromaDB com id: {doc_id}")

        collection.add(
            documents=[content],
            embeddings=[vector],
            metadatas=[metadata],
            ids=[doc_id]
        )

        logger.info("🎉 Upload concluído com sucesso")

        return {"status": "ok"}

    except Exception as e:
        logger.exception("🔥 ERRO NO UPLOAD")
        raise HTTPException(status_code=500, detail=str(e))