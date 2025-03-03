import logging
from datetime import datetime, timedelta, timezone
from typing import TypedDict
import uuid

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
    token_type: str # Token type (access or refresh)
    exp: int # Expiration time
    iat: int # Issued at
    aud: str # Audience
    iss: str # Issuer
    jti: str # JWT ID

class Token:
    def __init__(self, settings: TokenSettings):
        self.settings = settings

    def create_access_token(self, user_id: int, role: str) -> str:
        """
        Method to create an access token.
        Args:
            user_id (int): The user ID.
            role (str): The user role.
        Returns:
            str: The access token.
        Raises:
            Exception: If the token cannot be created.
        """
        try:
            time = datetime.now(timezone.utc)
            jti = str(uuid.uuid4()) 
            exp = int(( time + timedelta(minutes=self.settings.access_token_expire_minutes)).timestamp())
            claims: TokenClaims = {
                "user_id": user_id,
                "role": role,
                "token_type": "access",
                "exp": exp,
                "iat": int(time.timestamp()),
                "aud": self.settings.audience,
                "iss": self.settings.issuer,
                "jti": jti
            }
            return jwt.encode(claims, SECRET_KEY, algorithm=self.settings.algorithm)
        except Exception as e:
            logger.error(str(e))
            raise Exception("Could not create access token")

    def create_refresh_token(self, user_id: int, role: str) -> str:
        try:
            now = datetime.now(timezone.utc)
            jti = str(uuid.uuid4())
            exp = int((now + timedelta(days=self.settings.refresh_token_expire_days)).timestamp())
            claims: TokenClaims = {
                "user_id": user_id,
                "role": role,
                "token_type": "refresh",
                "exp": exp,
                "iat": int(now.timestamp()),
                "aud": self.settings.audience,
                "iss": self.settings.issuer,
                "jti": jti
            }
            return jwt.encode(claims, SECRET_KEY, algorithm=self.settings.algorithm)
        except Exception as e:
            logger.error(str(e))
            raise Exception("Could not create refresh token")


    def validate_token(self, token:str, roles: list[str]) -> TokenClaims:
        """
        Method to validate a token.
        Args:
            token (str): The token to validate.
            role (list[str]): The required role.
        Returns:
            TokenClaims: The token claims.
        Raises:
            jwt.ExpiredSignatureError: If the token has expired.
            jwt.InvalidTokenError: If the token is invalid.
            jwt.InvalidTokenError: If the user does not have the required role.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY,
                                algorithms=[self.settings.algorithm],
                                audience=self.settings.audience,
                                issuer=self.settings.issuer,
                                leeway=10, # Allow 10 seconds leeway
                                options={
                                    "require": ["exp", "iat", "aud", "iss", "jti"],
                                    "verify_signature": True,
                                }
                            )
            if payload["token_type"] != "access":
                raise jwt.InvalidTokenError("Invalid token type")
            if payload["role"] not in roles:
                raise jwt.InvalidTokenError("Insufficient permissions")
            return payload
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            raise jwt.ExpiredSignatureError("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.error(str(e))
            raise jwt.InvalidTokenError(str(e))
        except KeyError as e:
            logger.error("Missing required claim: %s", str(e))
            raise jwt.InvalidTokenError("Invalid token")
        
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
                                leeway=10, # Allow 10 seconds leeway
                                options={"require": ["exp", "jti", "iat", "aud", "iss", "token_type"]}
                                )
            if payload["token_type"] != "refresh":
                raise jwt.InvalidTokenError("Invalid token type")
            return self.create_access_token(payload["user_id"], payload["role"])
        except jwt.InvalidTokenError as e:
            logger.error(str(e))
            raise jwt.InvalidTokenError(str(e))
        except KeyError as e:
            logger.error("Missing required claim: %s", str(e))
            raise jwt.InvalidTokenError("Invalid token")
        except Exception as e:
            logger.error(str(e))
            raise Exception("Could not refresh access token")
