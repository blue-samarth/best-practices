# This file contains the APIResponse class which is used to standardize API responses.
from typing import Any

from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

class APIResponse(BaseModel):
    """
    This class is used to standardize API responses.
    """
    status_code: int 
    data: Any | None = None
    message: str | None = None
    status: str | None = None
    token: str | None = None
    meta: dict | None = None

    @classmethod
    def respond(cls, status_code: int, data: Any|None = None,
                message: str|None = None, status: str|None = None,
                token: str|None = None, meta: dict|None = None,
                headers: dict|None = None
                ) -> JSONResponse:
        """
        Return a JSONResponse object with standardized formatting.

        Args:
            status_code (int): The HTTP status code.
            data (Any): The response data.
            message (str): A message for the client.
            status (str): The response status, e.g., "success" or "error".
            token (str): An optional token for authentication.

        Returns:
            JSONResponse: The JSON response with properly encoded content.

        Raises:
            ValueError: If an invalid HTTP status code is provided.
        """


        if not (100 <= status_code < 600):
            raise ValueError(f"Invalid HTTP status code: {status_code}")
        
        if status_code == 204:
            return JSONResponse(status_code=status_code, content = None)
        
        response_body = {"data": data, "message": message, "status": status, "token": token, "meta": meta}

        response: dict = {key: value for key, value in response_body.items() if value is not None}

        encoded_response = jsonable_encoder(response)


        return JSONResponse(
            status_code=status_code,
            content=encoded_response,
            headers=headers
        )
