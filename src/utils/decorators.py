from functools import wraps
from typing import Awaitable

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from src.utils.authToken import Token, TokenSettings, InsufficientPermissionsError


oauth2passwordbearer = OAuth2PasswordBearer(tokenUrl="/login")
token_handler: Token = Token(TokenSettings())


def requires_auth(roles: list[str]|None) -> Awaitable[any]:
    """
    Decorator to enforce authentication.
    Args:
        roles (list[str]): The roles allowed to access the endpoint.
    Returns:
        bool: True if the user is authenticated, False otherwise.
    Raises:
        HTTPException: If the user is not authenticated.
    Usage:
        @app.get("/protected")
        @requires_auth(["admin"])
        def protected_route():
            return {"message": "This is a protected route"}
    """
    roles = roles or []
    def decorator(func) -> callable:
        @wraps(func)
        async def wrapper(*args, token: str = Depends(oauth2passwordbearer), **kwargs) -> callable:
            try:
                claims = token_handler.validate_token(token, roles)
            # Now if the error is this raise jwt.ExpiredSignatureError("Token has expired") we will return a 401
            except jwt.ExpiredSignatureError as e:
                raise HTTPException(status_code=401, detail=f"Token has expired: {str(e)}")
            # If the error is this raise jwt.InvalidTokenError("Invalid token type") we will return a 401
            except jwt.InvalidTokenError as e:
                raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
            # If the error is this raise jwt.InsufficientPermissionsError("Insufficient permissions") we will return a 401
            except InsufficientPermissionsError as e:
                raise HTTPException(status_code=403, detail=f"Insufficient permissions: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=401, detail=str(e))
            
            kwargs['claims'] = claims
            kwargs["user_id"] = claims["user_id"]
            kwargs["role"] = claims["role"]
            return await func(*args, **kwargs)
        return wrapper
    return decorator
