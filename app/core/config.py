import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # OpenRouter (novo provider de LLM + embeddings via base_url)
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    # Supabase (mantém igual)
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")


settings = Settings()