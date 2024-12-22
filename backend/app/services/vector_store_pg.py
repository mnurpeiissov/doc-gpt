import psycopg
from typing import List, Dict, Any
from app.core.config import settings
from app.services.interfaces import VectorStore

class PostgresVectorStore(VectorStore):
    def __init__(self):
        self.conn = psycopg.connect(
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT,
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD
        )

    def add_documents(self, docs: List[Any]) -> None:
        """
        docs is a list of tuples: (embedding, text, metadata)
        embedding: List[float]
        text: str
        metadata: dict with keys {document_id, document_name, paragraph_id, document_hash}
        """
        with self.conn.cursor() as cur:
            for emb, txt, meta in docs:
                cur.execute("""
                    INSERT INTO documents (id, text, document_name, document_id, paragraph_id, document_hash, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (
                    f"{meta['document_id']}_{meta['paragraph_id']}",
                    txt,
                    meta["document_name"],
                    meta["document_id"],
                    meta["paragraph_id"],
                    meta["document_hash"],
                    emb
                ))
        self.conn.commit()

    def search(self, query_embedding: List[float], top_k: int = 5, threshold: float = 0.75) -> List[Dict]:
        """
        Search for similar documents based on the provided query embedding.

        Args:
            query_embedding (List[float]): The embedding vector of the query.
            top_k (int): Number of top results to return. Default is 5.
            threshold (float): Minimum similarity score to include a result. Default is 0.75.

        Returns:
            List[Dict]: A list of matching documents with their metadata and similarity scores.
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
        with self.conn.cursor() as cur:
            try:
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
            except Exception as e:
                raise RuntimeError(f"Error executing search query: {e}")
        return results
    
    def get_paragraph(self, doc_id, paragraph_id):
        with self.conn.cursor() as cur:
            try:
                cur.execute("""               
                    SELECT text
                    FROM documents
                    WHERE document_id = %s AND paragraph_id = %s
                """,(doc_id, paragraph_id))
            except Exception as e:
                raise RuntimeError(f"Error fetching the paragraph: {e}")
            return cur.fetchone()

    def exists(self, doc_hash):
        with self.conn.cursor() as cur:
            try:
                cur.execute("""
                    SELECT 1 FROM documents WHERE document_hash = %s
                """, (doc_hash,))
            except Exception as e:
                raise RuntimeError(f"Error checking existence {e}")
            return True if cur.fetchone() else False