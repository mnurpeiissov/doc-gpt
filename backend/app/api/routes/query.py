from fastapi import APIRouter, HTTPException
from app.models import QueryRequest
from app.models import QueryResponse
from app.services.llm_openai import OpenAILLM
from app.services.guardrails import validate_answer_references
from app.services.embedder_openai import OpenAIEmbedder
from app.api.deps import VectorStore
from app.core.config import settings

router = APIRouter(tags=["query"])

@router.post("", response_model=QueryResponse)
def query_documents(
    vector_store: VectorStore,
    request: QueryRequest
):
    query = request.query.strip()
    query_embs = OpenAIEmbedder().get_embeddings(query)
    if not query:
        raise HTTPException(status_code=400, detail="Query is empty.")
    results = vector_store.search(query_embs, top_k=5, threshold=0.75)
    if not results:
        return QueryResponse(answer="This question is not applicable to the current documents.", document_link=None)
    context = ""
    meta_data_list = []
    for doc in results:
        paragraph = doc["text"]
        doc_name = doc["metadata"]["document_name"]
        doc_id = doc["metadata"]["document_id"]
        p_id = doc["metadata"]["paragraph_id"]
        context += f"(Document: {doc_name}, Paragraph: {p_id}, Document_id: {doc_id}) {paragraph},\n\n"
        meta_data_list.append((doc_name, p_id, doc_id))
    answer = OpenAILLM().generate_answer(query, context)
    doc_link = validate_answer_references(answer, meta_data_list)
    if doc_link is None:
        return QueryResponse(answer="This question is not applicable to the current documents.", document_link=None)
    link = f"{settings.APP_BASE_URL}{settings.API_V1_STR}/documents/view/{doc_link['doc_id']}?paragraph_id={doc_link['p_id']}"
    return QueryResponse(answer=answer, document_link=link)
