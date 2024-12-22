import uuid
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.embedder_openai import OpenAIEmbedder
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.api.deps import SessionDep, VectorStore
from app.models import ParagraphResponse
import os
from pdfplumber import open as open_pdf
from docx import Document
from io import BytesIO
import hashlib


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
    vector_store: VectorStore,
    files: List[UploadFile] = File(...)
):
    for file in files:
        doc_id = str(uuid.uuid4())
        content = await file.read()
        file_hash = hashlib.md5(content).hexdigest()
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
        else:
            raise ValueError("Unsupported file format. Please upload a .txt, .docx, or .pdf file.")
        # splitter = RecursiveCharacterTextSplitter(
        #     separators=["\n\n"],
        #     chunk_size=500,
        #     chunk_overlap=50
        # )
        # paragraphs = splitter.split_text(text)
        paragraphs = split_text_into_chunks(text)
        if not paragraphs:
            raise HTTPException(status_code=400, detail=f"Could not parse {file.filename}")
        embedder = OpenAIEmbedder()
        embeddings = [embedder.get_embeddings(paragraph) for paragraph in paragraphs]
        docs = []
        for i, paragraph in enumerate(paragraphs):
            metadata = {
                "document_id": doc_id,
                "document_name": file.filename,
                "paragraph_id": i + 1,
                "document_hash": file_hash
            }
            docs.append((embeddings[i], paragraph, metadata))
        vector_store.add_documents(docs)
        
    return {"status": "documents indexed successfully"}


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