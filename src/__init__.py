import asyncio
from fastapi import FastAPI
from src.db import init_db, generate_schema, close_connection

app: FastAPI = FastAPI()

async def startup_db_client() -> None:
    """Initialize the database connection."""
    await init_db()
    await generate_schema()

async def shutdown_db_client() -> None:
    """Close the database connection."""
    await close_connection()
