import hashlib
import os
import uuid
from io import BytesIO

from app.core.config import settings
from app.services.embedder_openai import OpenAIEmbedder
from app.services.vector_store_pg import PostgresVectorStore
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pdfplumber import open as open_pdf

if settings.INITIAL_DATA_DIR:
    vector_store = PostgresVectorStore()
    files = os.listdir(settings.INITIAL_DATA_DIR)

    for file in files:
        doc_id = str(uuid.uuid4())
        with open(file, 'r') as fp:
            content = fp.read()
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
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n"],
            chunk_size=500,
            chunk_overlap=50
        )
        paragraphs = splitter.split_text(text)
        if not paragraphs:
            continue
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
    vector_store.conn.close()