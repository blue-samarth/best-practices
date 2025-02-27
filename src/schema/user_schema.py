from datetime import datetime
from pydantic import BaseModel, EmailStr, validator
from tortoise.contrib.pydantic import pydantic_model_creator

class UserCreate(BaseModel):
    """A user creation model."""
    email: EmailStr
    password: str
    name: str

    @validator("password")
    def validate_password(cls, password: str) -> str:
        """
        Validate the password.
        Requirements:
            - At least 8 characters long
            - At least one uppercase letter
            - At least one lowercase letter
            - At least one digit
            - At least one special character
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        if not any(not char.isalnum() for char in password):
            raise ValueError("Password must contain at least one special character")
        
        return password

class UserViewAdmin(BaseModel):
    """A user view model for administrators."""
    id: int
    email: EmailStr
    name: str
    created_at: datetime
    updated_at: datetime

class UserViewPublic(BaseModel):
    """A user view model for the public."""
    name: str
    email: EmailStr
    created_at: datetime

User_Pydantic = pydantic_model_creator(User, name="User", exclude=("id",))
