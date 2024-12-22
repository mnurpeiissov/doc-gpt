from app.api.routes import documents, query
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(query.router, prefix='/query')
api_router.include_router(documents.router, prefix='/documents')
