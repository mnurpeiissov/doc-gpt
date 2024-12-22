from typing import Any, Dict, List

from app.core.config import settings
from app.services.interfaces import VectorStore
from psycopg_pool import ConnectionPool


class PostgresVectorStore(VectorStore):
    def __init__(self, pool: ConnectionPool):
        """
        Initialize the vector store with a connection pool.

        Args:
            pool (ConnectionPool): A psycopg connection pool instance.
        """
        self.pool = pool

    def add_documents(self, docs: List[Any]) -> None:
        """
        Add documents to the database.
        """
        query = """
            INSERT INTO documents (id, text, document_name, document_id, paragraph_id, document_hash, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                for emb, txt, meta in docs:
                    cur.execute(query, (
                        f"{meta['document_id']}_{meta['paragraph_id']}",
                        txt,
                        meta["document_name"],
                        meta["document_id"],
                        meta["paragraph_id"],
                        meta["document_hash"],
                        emb
                    ))
            conn.commit()

    def search(self, query_embedding: List[float], top_k: int = 5, threshold: float = 0.75) -> List[Dict]:
        """
        Search for similar documents.
        """
        emb_str = f"ARRAY[{', '.join(map(str, query_embedding))}]::vector"
        query = f"""
            SELECT 
                text, 
                document_name, 
                document_id, 
                paragraph_id, 
                1 - (embedding <#> {emb_str}) AS similarity
            FROM documents
            ORDER BY embedding <#> {emb_str}
            LIMIT %s
        """
        results = []
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (top_k,))
                rows = cur.fetchall()
                for r in rows:
                    text, doc_name, doc_id, p_id, sim = r
                    if sim >= threshold:
                        results.append({
                            "text": text,
                            "metadata": {
                                "document_name": doc_name,
                                "document_id": doc_id,
                                "paragraph_id": p_id
                            },
                            "score": sim
                        })
        return results

    def get_paragraph(self, doc_id, paragraph_id):
        """
        Retrieve paragraph text 
        """
        query = """
            SELECT text
            FROM documents
            WHERE document_id = %s AND paragraph_id = %s
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (doc_id, paragraph_id))
                return cur.fetchone()

    def exists(self, doc_hash):
        """
        Check if the document exists
        """
        query = """
            SELECT 1 FROM documents WHERE document_hash = %s
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (doc_hash,))
                return True if cur.fetchone() else False
