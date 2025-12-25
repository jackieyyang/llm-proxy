from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db_config import init_db_connection, close_db_connection
from .httpx_config import init_httpx_client, close_httpx_client


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Initialize resources
    await init_db_connection()
    await init_httpx_client()

    yield

    # Cleanup resources
    await close_db_connection()
    await close_httpx_client()