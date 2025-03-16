# src/__init__.py
# This file contains the FastAPI app and the lifespan context manager.
import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.db import init_db, generate_schema, close_connection

load_dotenv(dotenv_path='src/.env')
SECRET_KEY = os.getenv('SECRET_KEY')
DB_URL = os.getenv('DB_URL', 'sqlite://db.sqlite3')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '8000'))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# print(type(SECRET_KEY), type(DB_URL), type(HOST), type(PORT), type(DEBUG))

@asynccontextmanager
async def lifespan(app: FastAPI, DB_URL: str = DB_URL):
    # Startup code: initialize the database connection and generate the schema.
    print("Starting up: initializing DB and generating schema...")
    await init_db(DB_URL)
    await generate_schema()
    
    # Yield control to the app (the app runs during this period).
    yield
    
    # Shutdown code: close the database connection.
    print("Shutting down: closing DB connection...")
    await close_connection()

app: FastAPI = FastAPI(
    title="FastAPI user",
    description="A simple user management API",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
