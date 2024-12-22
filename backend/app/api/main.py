from fastapi import APIRouter
from app.api.routes import query, documents

api_router = APIRouter()
api_router.include_router(query.router, prefix='/query')
api_router.include_router(documents.router, prefix='/documents')
