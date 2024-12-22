from app.core.config import settings
from app.services.vector_store_pg import PostgresVectorStore
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
        CREATE INDEX ON documents USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
        """)
    conn.commit()
    conn.close()
vector_store.pool.close()