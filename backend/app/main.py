from app.api.main import api_router
from app.core.config import settings
from app.services.vector_store_pg import PostgresVectorStore
from fastapi import FastAPI
from fastapi.routing import APIRoute
from psycopg_pool import ConnectionPool
from starlette.middleware.cors import CORSMiddleware


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

@app.on_event("startup")
def setup_vector_store():
    pool = ConnectionPool(conninfo=f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    app.state.vector_store = PostgresVectorStore(pool)

@app.on_event("shutdown")
def close_vector_store():
    app.state.vector_store.pool.close()



#Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)