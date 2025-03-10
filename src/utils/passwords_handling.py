from datetime import datetime, timedelta, timezone
import secrets
from passlib.context import CryptContext

class PasswordHandle:
    """
    Class to handle password hashing and verification
    """
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["argon2", "bcrypt"],
            default="argon2",
            deprecated="auto"
        )

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        This method hashes a password
        Args:
            password (str): The password to hash
        Returns:
            str: The hashed password
        """
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Method to verify a password
        Args:
            plain_password (str): The plain password
            hashed_password (str): The hashed password
        Returns:
            bool: True if the password is verified, False otherwise
        """
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def generate_reset_token(cls, expiry_time: int = 30,
                            email: str|None = None,
                            user_id: int|None = None
                        ) -> tuple: 
        """
        Generate a secure token to reset a password with expiration time
        Args:
            expiry_time (int): The time in minutes before the token expires
            email (str): The email of the user
            user_id (int): The user ID
        Returns:
            tuple: The token and the expiration time
        """
        if not email and not user_id:
            raise ValueError("You must provide an email or user_id")
        
        token = secrets.token_urlsafe(32)
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=expiry_time)
        return token, expiration_time
