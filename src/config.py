# Here we will define the secret key for the JWT token.
import os
import argparse

from secrets import token_urlsafe

class Config:
    """
    This class will hold all the configurations for the application.
    """

    __slots__ = ["SECRET_KEY", "DB_URL", "HOST", "PORT", "DEBUG", "size_of_token"]

    def __init__(self, size_of_token: int = 32, db_url: str = "sqlite://db.sqlite3",
                 host: str = "0.0.0.0", port: int = 8000, debug: bool = False
                 ) -> None:
        self.size_of_token = size_of_token
        self.SECRET_KEY = os.getenv("SECRET_KEY", token_urlsafe(self.size_of_token))
        self.DB_URL = db_url
        self.HOST = host
        self.PORT = port
        self.DEBUG = debug

    def get_secret_key(self) -> str:
        """Return the secret key."""
        return self.SECRET_KEY
    
    def add_in_env(self) -> None:
        """Add the all the configurations in the environment."""
        os.environ["SECRET_KEY"] = self.SECRET_KEY
        os.environ["DB_URL"] = self.DB_URL
        os.environ["HOST"] = self.HOST
        os.environ["PORT"] = str(self.PORT)
        os.environ["DEBUG"] = str(self.DEBUG)

    def remove_from_env(self, key: str) -> None:
        """Remove the configuration from the environment."""
        if key in os.environ.keys():
            os.environ.pop(key)

    def clear_app_env(self) -> None:
        """Clear the configurations from the environment."""
        for key in ['SECRET_KEY', 'DB_URL', 'HOST', 'PORT', 'DEBUG']:
            if key in os.environ.keys():
                os.environ.pop(key)

    def __str__(self) -> str:
        return f"Config(DB_URL={self.DB_URL}, HOST={self.HOST}, PORT={self.PORT}, DEBUG={self.DEBUG})"
    
    def __repr__(self) -> str:
        return (
            f"Config(DB_URL={self.DB_URL}, HOST={self.HOST}, PORT={self.PORT}, "
            f"DEBUG={self.DEBUG}, SECRET_KEY='***HIDDEN***')"
        )

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configuration for the application.")
    parser.add_argument("--size_of_token", type=int, default=32, help="Size of the token.")
    parser.add_argument("--db_url", type=str, default="sqlite://db.sqlite3", help="Database URL.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host for the application.")
    parser.add_argument("--port", type=int, default=8000, help="Port for the application.")
    parser.add_argument("--debug", type=lambda x: x.lower() in ["true", "1"], default=False, help="Debug mode.")
    args = parser.parse_args()

    config = Config(size_of_token=args.size_of_token, db_url=args.db_url, host=args.host, port=args.port, debug=args.debug)
    config.add_in_env()
    print(config)
