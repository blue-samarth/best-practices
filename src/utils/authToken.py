import logging
from datetime import datetime, timedelta, timezone
from typing import TypedDict

import jwt
from pydantic import BaseSettings


from src import SECRET_KEY

logger = logging.getLogger(__name__)

class TokenSettings(BaseSettings):
    """Token settings."""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    issuer: str = "fastapi-tortoise"
    audience: str = "api-frontend"

class TokenClaims(TypedDict):
    """Token claims."""
    user_id: int
    role: str
    exp: int # Expiration time
    iat: int # Issued at
    aud: str # Audience
    iss: str # Issuer
    jti: str # JWT ID

class Token:
    def __init__(self, settings: TokenSettings):
        self.settings = settings

    def create_access_token(self, user_id: int, role: str, jti: str) -> str:
        """
        Method to create an access token.
        Args:
            user_id (int): The user ID.
            role (str): The user role.
            jti (str): The JWT ID.
        Returns:
            str: The access token.
        Raises:
            Exception: If the token cannot be created.
        """
        try:
            exp = int((datetime.now(timezone.utc) + timedelta(minutes=self.settings.access_token_expire_minutes)).timestamp())
            claims: TokenClaims = {
                "user_id": user_id,
                "role": role,
                "exp": exp,
                "iat": int(datetime.now(timezone.utc).timestamp()),
                "aud": self.settings.audience,
                "iss": self.settings.issuer,
                "jti": jti
            }
            return jwt.encode(claims, SECRET_KEY, algorithm=self.settings.algorithm)
        except Exception as e:
            logger.error(str(e))
            raise Exception("Could not create access token")

    def validate_token(self, token:str, roles: list[str]) -> TokenClaims:
        """
        Method to validate a token.
        Args:
            token (str): The token to validate.
            role (list[str]): The required role.
        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY,
                                algorithms=[self.settings.algorithm],
                                audience=self.settings.audience,
                                issuer=self.settings.issuer,
                                options={"require": ["exp", "iat", "aud", "iss"]}
                                )
            if payload["role"] not in roles:
                raise jwt.InvalidTokenError("Insufficient permissions")
            
            return payload
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            raise jwt.ExpiredSignatureError("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.error(str(e))
            raise jwt.InvalidTokenError(str(e))
        
    def refresh_access_token(self, token: str) -> str:
        """
        Method to refresh an access token.
        Args:
            token (str): The token to refresh.
        Returns:
            str: The refreshed access token.
        Raises:
            Exception: If the token cannot be refreshed.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY,
                                algorithms=[self.settings.algorithm],
                                audience=self.settings.audience,
                                issuer=self.settings.issuer,
                                options={"require": ["exp", "iat", "aud", "iss"]}
                                )
            return self.create_access_token(payload["user_id"], payload["role"], payload["jti"])
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            raise jwt.ExpiredSignatureError("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.error(str(e))
            raise jwt.InvalidTokenError(str(e))
        except Exception as e:
            logger.error(str(e))
            raise Exception("Could not refresh access token")
