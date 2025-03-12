# This file contains the APIResponse class which is used to standardize API responses.
from typing import Any

from pydantic import BaseModel
from fastapi.responses import JSONResponse

class APIResponse(BaseModel):
    """
    This class is used to standardize API responses.
    """
    status_code: int 
    data: Any | None = None
    message: str | None = None
    status: str | None = None
    token: str | None = None

    @classmethod
    def respond(cls, status_code: int, data: Any|None = None,
                message: str|None = None, status: str|None = None,
                token: str|None = None
                ) -> JSONResponse:
        """
        A class method to return a JSONResponse object.
        Args:
            status_code (int): The status code.
            data (Any): The data to return.
            message (str): The message to return.
            status (str): The status to return.
            token (str): The token to return.
        Returns:
            JSONResponse: The JSONResponse object.
        Raises:
            ValueError: If the status code is not a valid HTTP status code.
        """

        if not (100 <= status_code < 600):
            raise ValueError(f"Invalid HTTP status code: {status_code}")
        
        if status_code == 204:
            return JSONResponse(
                status_code=status_code,
                content = None
            )
        
        response_body = {
            "data": data,
            "message": message,
            "status": status,
            "token": token
        }

        response: dict = {key: value for key, value in response_body.items() if value is not None}


        return JSONResponse(
            status_code=status_code,
            content={k: v for k, v in response.items() if k not in {'status_code'} and v is not None}
        )
