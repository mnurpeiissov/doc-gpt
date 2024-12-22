from pydantic import BaseModel
from typing import Optional

class QueryResponse(BaseModel):
    answer: str
    document_link: Optional[str] = None

class QueryRequest(BaseModel):
    query: str

class ParagraphResponse(BaseModel):
    doc_id: str
    paragraph_id: int
    text: str
