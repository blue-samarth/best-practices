from datetime import datetime
from functools import wraps

from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer

from src.utils.authToken import Token


outh2passwordbearer = OAuth2PasswordBearer(tokenUrl="/login")

def requires_auth(role: list[str]) -> callable:
    """Check if the user is authenticated."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, token: str = Depends(outh2passwordbearer), **kwargs) -> None:
            if Token.is_token_expired(token):
                raise HTTPException(status_code=401, detail="Token has expired")
            if not Token.check_role(token, role):
                raise HTTPException(
                    status_code=403,
                    detail=f"User does not have the required role: {', '.join(role)}")
            payload = Token.decode_token(token)
            kwargs['user_id'] = payload['user_id']
            kwargs['role'] = payload['role']
            return await func(*args, **kwargs)
        return wrapper
    return decorator
