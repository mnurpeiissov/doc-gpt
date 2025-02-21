import uuid
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.embedder_openai import OpenAIEmbedder
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.api.deps import SessionDep, VectorStore
from app.models import ParagraphResponse, FHIR, FHIRRecord
import os
from pdfplumber import open as open_pdf
from docx import Document
from io import BytesIO
import hashlib
import base64
from app.services.llm_openai import OpenAILLM
from tiktoken import get_encoding

def split_text_into_chunks(text, max_tokens=1000, overlap=50):
    tokenizer = get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    
    chunks = []
    for i in range(0, len(tokens), max_tokens - overlap):
        chunk = tokens[i:i + max_tokens]
        chunks.append(tokenizer.decode(chunk))
    
    return chunks


router = APIRouter(tags=["documents"])

@router.post("")
async def upload_documents(
    user_id: int,
    vector_store: VectorStore,
    db: SessionDep, 
    files: List[UploadFile] = File(...)
):
    for file in files:
        doc_id = str(uuid.uuid4())
        content = await file.read()
        file_hash = hashlib.md5(content).hexdigest()
        parsed_data = None
        if vector_store.exists(file_hash):
            continue
        _, file_extension = os.path.splitext(file.filename.lower())
        if file_extension == ".txt":
            text = content.decode("utf-8", errors="ignore")
        elif file_extension == ".docx":
            with BytesIO(content) as docx_file:
                doc = Document(docx_file)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        elif file_extension == ".pdf":
            with BytesIO(content) as pdf_file:
                text = ""
                with open_pdf(pdf_file) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
        elif file_extension in ('.jpg', '.png', 'jpeg'):
            encoded_image = base64.b64encode(content).decode('ascii')
            parsed_data = OpenAILLM().parse_json(is_img=True, base64_image=encoded_image)
        else:
            raise ValueError("Unsupported file format. Please upload a .txt, .docx, or .pdf file.")

        if not parsed_data:
            parsed_data = OpenAILLM().parse_json(text)
        
        fhir_data = OpenAILLM().convert_to_fhir(parsed_data, user_id)
        
        db_record = FHIRRecord(
            patient_id=user_id, 
            fhir_data=fhir_data, 
            created_at = 'now'
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        
    return {"status": "Documents successfully parsed"}


@router.get('/view/{doc_id}', response_model=ParagraphResponse)
def view_document(
    vector_store: VectorStore,
    doc_id: str, 
    paragraph_id: int
) -> ParagraphResponse:
    doc = vector_store.get_paragraph(doc_id, paragraph_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document or paragraph not found")
    return ParagraphResponse(doc_id=doc_id, paragraph_id=paragraph_id, text=doc[0])


@router.get('/view')
def get_fhir_data(patient_id: str, db: SessionDep, language: str):
    records = db.query(FHIRRecord).filter(FHIRRecord.patient_id == patient_id).all()
    
    if not records:
        raise HTTPException(status_code=404, detail="FHIR records not found for this patient")

    translated_records = [
        {
            "patient_id": record.patient_id,
            "fhir_data": OpenAILLM().translate_to_language(record.fhir_data, language)
        }
        for record in records
    ]

    return {"patient_id": patient_id, "records": translated_records}



[
  {
    "id": "rec_123",
    "type": "Lab Result",
    "title": "Blood Test - CBC",
    "patientName": "John Doe",
    "date": "2024-02-15T10:30:00Z",
    "fileUrl": "https://cloudstorage.com/record123.pdf",
    "hospitalName": "City Hospital",
    "doctorName": "Dr. Alice Smith",
    "notes": "<b>Slight anemia detected.</b> <a href='https://hospital.com/report'>View Full Report</a>"
  }, 
  {

  }
]
