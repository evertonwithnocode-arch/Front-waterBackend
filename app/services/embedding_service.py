from langchain_openai import OpenAIEmbeddings
from app.core.config import settings

embeddings = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)