import os

from langchain_openai import OpenAIEmbeddings
from app.core.config import settings


embeddings = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    check_embedding_ctx_length=False,
    model_kwargs={"encoding_format": "float"}
)