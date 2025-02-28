# import asyncio
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.db import init_db, generate_schema, close_connection

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

async def startup_db_client() -> None:
    """Initialize the database connection."""
    await init_db()
    await generate_schema()

async def shutdown_db_client() -> None:
    """Close the database connection."""
    await close_connection()

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
