import logging
from datetime import datetime, timedelta

import jwt
from pydantic import BaseModel

from src import SECRET_KEY

logger = logging.getLogger(__name__)

class Token(BaseModel):
    """It is a class to generate and verify JWT tokens."""
    user_id: int
    exp: int
    role: str

    def __init__(self, user_id: int, role: str, exp_in: int = 60) -> None:
        """
        Initialize the Token class.
        Args:
            user_id (int): The user id.
            role (str): The user role.
            exp_in (int): The expiration time in minutes.
        
        """
        exp = int(datetime.now() + timedelta(minutes=exp_in).timestamp())
        super().__init__(user_id=user_id, exp=exp, role=role)

    def create_token(self) -> str:
        """Create a JWT token."""
        payload = {
            'user_id': self.user_id,
            'exp': int((datetime.now() + timedelta(minutes=self.exp)).timestamp()),
            'role': self.role
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode a JWT token."""
        if not token:
            logger.error('Token not found.')
            return None
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            logger.error('Token expired.')
            return None
        except jwt.InvalidTokenError:
            logger.error('Invalid token.')
            return None
        
    @classmethod
    def check_role(cls, token: str, role: str) -> bool:
        """Check if the token has the required role."""
        decoded_token = cls.decode_token(token)
        if not decoded_token:
            return False
        return decoded_token['role'] == role
    
    # now we will check if the token has expired or not

    @staticmethod
    def is_token_expired(token: str) -> bool:
        """Check if the token has expired."""
        decoded_token = Token.decode_token(token)
        if not decoded_token:
            return True
        return datetime.fromtimestamp(decoded_token['exp']) < datetime.now()

    @classmethod
    def check_token(cls, token: str, role: str) -> bool:
        """Check if the token is valid and has the required role."""
        decoded_token = cls.decode_token(token)
        if not decoded_token:
            return False
        return decoded_token['role'] == role and datetime.fromtimestamp(decoded_token['exp']) > datetime.now()

    @classmethod
    def refresh_token(cls, token: str, expires_in: int = 60) -> str:
        """Refresh the token."""
        decoded_token = cls.decode_token(token)
        if not decoded_token:
            return None
        return cls(decoded_token['user_id'],
                   decoded_token['role'],
                   expires_in
                ).create_token()
