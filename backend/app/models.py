from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import date, datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, JSON, TIMESTAMP
from datetime import datetime
from typing import List, Dict, Any
from app.core.db import engine

class QueryResponse(BaseModel):
    answer: str
    document_link: Optional[str] = None

class QueryRequest(BaseModel):
    query: str

class ParagraphResponse(BaseModel):
    doc_id: str
    paragraph_id: int
    text: str

class FHIR(BaseModel):
    id: Optional[str] = None
    patient_id: int 
    fhir_data: dict
    created_at: str


Base = declarative_base()

# Define FHIR Database Model
class FHIRRecord(Base):
    __tablename__ = "fhir_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, nullable=False)
    fhir_data = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class FHIRSchema(BaseModel):
    patient_id: str
    fhir_data: Dict[str, Any]

Base.metadata.create_all(bind=engine)