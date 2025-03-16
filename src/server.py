# src/server.py
# This file is the entry point of the application. It starts the FastAPI application and runs it using Uvicorn.
import uvicorn

from src import app
from src import HOST, PORT, DEBUG
from src.api.login_signup import user_log_sign_in_router

app.include_router(user_log_sign_in_router, prefix="/api/v1")

def start() -> None:
    """Start the application."""
    uvicorn.run("src.server:app", host=HOST, port=PORT, reload=DEBUG)


@app.get("/", tags=["root"]) #tags is used to group the endpoints in the swagger UI
async def read_root() -> dict:
    """Root endpoint."""
    return {"message": "Welcome to your user management API!"}

@app.get("/health", tags=["root"])
async def health_check() -> dict:
    """Health check endpoint."""
    return {"message": "OK"}


if __name__ == "__main__":
    start()
