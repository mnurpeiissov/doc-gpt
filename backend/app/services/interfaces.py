from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorStore(ABC):
    @abstractmethod
    def add_documents(self, docs: List[Any]) -> None:
        pass

    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int = 5, threshold: float = 0.75) -> List[Dict]:
        pass
    
    @abstractmethod
    def get_paragraph(self, doc_id: str, paragraph_id: int) -> str:
        pass

    @abstractmethod
    def exists(self, doc_hash:str) -> bool:
        pass

class LLM(ABC):
    @abstractmethod
    def generate_answer(self, query: str, context: str) -> str:
        pass


class EMBEDDER(ABC):
    @abstractmethod
    def get_embeddings(self,texts: List[str]) -> List[float]:
        pass

