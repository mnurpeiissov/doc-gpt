from app.services.vector_store_pg import PostgresVectorStore
from app.core.config import settings
from psycopg_pool import ConnectionPool

pool = ConnectionPool(conninfo=f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")

vector_store = PostgresVectorStore(pool)

with vector_store.pool.connection() as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            text TEXT,
            document_name TEXT,
            document_id TEXT,
            paragraph_id INT,
            document_hash TEXT,
            embedding vector(1536)
        );
        """)
    conn.commit()
    
    with conn.cursor() as cur:
        cur.execute(
        """
            CREATE TABLE IF NOT EXISTS fhir_records (
            id SERIAL PRIMARY KEY,
            patient_id TEXT NOT NULL,
            fhir_data JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );         
        """)
    conn.commit()
    
    
    
    
    
    conn.close()
vector_store.pool.close()