from fastapi import FastAPI

from src import app, startup_db_client, shutdown_db_client


async def init_app() -> FastAPI:
    """Initialize the application."""
    app.add_event_handler("startup", startup_db_client)
    app.add_event_handler("shutdown", shutdown_db_client)

    return app

app: FastAPI = FastAPI(title="FastAPI user",description="A simple user management API",version="0.1.0")

# app.include_router(, prefix="/users", tags=["users"])

def start() -> None:
    """Start the application."""
    import uvicorn
    uvicorn.run("src.server:app", host="0.0.0.0", port=8000, reload=True)

@app.get("/", tags=["root"]) #tags is used to group the endpoints in the swagger UI
async def read_root() -> dict:
    """Root endpoint."""
    return {"message": "Welcome to your user management API!"}

@app.get("/health", tags=["root"])
async def health_check() -> dict:
    """Health check endpoint."""
    return {"message": "OK"}


app = init_app()

if __name__ == "__main__":
    start()