# This file contains the decorators used to enforce authentication and authorization in the application.
import inspect
from functools import wraps
from typing import Awaitable

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from src.utils.authToken import Token, TokenSettings, InsufficientPermissionsError


oauth2passwordbearer = OAuth2PasswordBearer(tokenUrl="/login")
token_handler: Token = Token(TokenSettings())


def requires_auth(roles: list[str]|None = None) -> callable:
    """
    Decorator to enforce authentication.
    Args:
        roles (list[str]): The roles allowed to access the endpoint.
    Returns:
        The decorated function.
    Raises:
        HTTPException: If the user is not authenticated.
    Usage:
        @app.get("/protected")
        @requires_auth(["admin"])
        async def protected_route():
            return {"message": "This is a protected route"}
    """
    roles = roles or []
    def decorator(func) -> callable:
        @wraps(func)
        async def wrapper(*args, token: str = Depends(oauth2passwordbearer), **kwargs) -> Awaitable:
            try:
                print("Token: ", token)
                claims = token_handler.validate_token(token, roles)
                sig: inspect.Signature = inspect.signature(func)
                accepted_params: list[str] = list(sig.parameters.keys())
                extra_kwargs: dict = {
                    "token_user_id": claims.get("user_id"),
                    "token_role": claims.get("role"),
                }

                filtered_kwargs: dict = {k: v for k, v in extra_kwargs.items() if k in accepted_params}
                kwargs.update(filtered_kwargs)
                return await func(*args, **kwargs)

            except jwt.ExpiredSignatureError as e:
                raise HTTPException(status_code=401, detail=f"Token has expired: {str(e)}")
            except jwt.InvalidTokenError as e:
                raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
            except InsufficientPermissionsError as e:
                raise HTTPException(status_code=403, detail=f"Insufficient permissions: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=401, detail=str(e))

        wrapper.__signature__ = inspect.signature(func)
        return wrapper
    return decorator
