from app.services.vector_store_pg import PostgresVectorStore

vector_store = PostgresVectorStore()

with vector_store.conn.cursor() as cur:
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
vector_store.conn.commit()
vector_store.conn.close()