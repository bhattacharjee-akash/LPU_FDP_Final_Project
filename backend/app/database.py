from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from supabase import create_client, Client
from app.config import settings

# SQLAlchemy setup
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL and "?" in DATABASE_URL:
    base_url, query_str = DATABASE_URL.split("?", 1)
    params = [p for p in query_str.split("&") if not p.startswith("pgbouncer")]
    if params:
        DATABASE_URL = f"{base_url}?{'&'.join(params)}"
    else:
        DATABASE_URL = base_url
print(f"Database connection string resolved to: {DATABASE_URL.split('@')[-1] if DATABASE_URL else 'None'}")

engine = None

if not DATABASE_URL or "localhost" in DATABASE_URL or "127.0.0.1" in DATABASE_URL:
    try:
        # Check if local postgres is running
        temp_engine = create_engine(DATABASE_URL)
        # Try to connect with a short timeout check
        with temp_engine.connect() as conn:
            pass
        engine = temp_engine
    except Exception:
        # Fallback to local SQLite for zero-setup execution
        sqlite_url = "sqlite:///./local_copilot.db"
        print(f"PostgreSQL local connection refused. Falling back to local SQLite: {sqlite_url}")
        engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Supabase SDK setup
supabase_url = settings.SUPABASE_URL
supabase_key = settings.SUPABASE_ANON_KEY
supabase_service_key = settings.SUPABASE_SERVICE_ROLE_KEY

supabase_client: Client = None
supabase_admin: Client = None

if supabase_url and supabase_key:
    supabase_client = create_client(supabase_url, supabase_key)
if supabase_url and supabase_service_key:
    supabase_admin = create_client(supabase_url, supabase_service_key)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
