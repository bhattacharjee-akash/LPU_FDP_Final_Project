import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "LPU Academic Copilot"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/postgres"
    
    # Supabase Credentials
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    
    # LLM Provider Keys
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    
    # Defaults
    DEFAULT_LLM_PROVIDER: str = "gemini" # gemini or groq
    DEFAULT_GEMINI_MODEL: str = "gemini-2.5-flash"
    DEFAULT_GROQ_MODEL: str = "mixtral-8x7b-32768"
    DEFAULT_TEMPERATURE: float = 0.7
    
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

# Clean DATABASE_URL for compatibility with psycopg2 (strip pgbouncer option)
if settings.DATABASE_URL:
    if "?" in settings.DATABASE_URL:
        base_url, query_str = settings.DATABASE_URL.split("?", 1)
        params = [p for p in query_str.split("&") if not p.startswith("pgbouncer")]
        if params:
            settings.DATABASE_URL = f"{base_url}?{'&'.join(params)}"
        else:
            settings.DATABASE_URL = base_url
