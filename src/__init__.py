# import asyncio
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.db import init_db, generate_schema, close_connection

load_dotenv('.env')
SECRET_KEY = os.getenv('SECRET_KEY')
DB_URL = os.getenv('DB_URL', 'sqlite://db.sqlite3')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '8000'))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

app: FastAPI = FastAPI(
    title="FastAPI user",
    description="A simple user management API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event("startup")
async def startup_db_client() -> None:
    """Initialize the database connection."""
    await init_db(DB_URL)
    await generate_schema()

@app.on_event("shutdown")
async def shutdown_db_client() -> None:
    """Close the database connection."""
    await close_connection()
