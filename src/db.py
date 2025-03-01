# This file contains the database initialization and schema generation functions.
from logging import getLogger

from tortoise import Tortoise

logger = getLogger  (__name__)
MODELS = ["models.user",
          ]

async def init_db(db_url: str|None = None) -> None:
    """Initialize the database connection."""
    db_url = db_url or "sqlite://db.sqlite3"

    await Tortoise.init(
        db_url=db_url,
        modules={"models": MODELS},
    )
    logger.info(f"Connecting to database: {db_url}")

async def generate_schema() -> None:
    """Generate the database schema."""
    await Tortoise.generate_schemas()
    logger.info("Generating database schema")

async def close_connection() -> None:
    """Close the database connection."""
    await Tortoise.close_connections()
    logger.info("Closing database connection")
