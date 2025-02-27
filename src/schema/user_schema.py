from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator
from tortoise.contrib.pydantic import pydantic_model_creator

from src.models.users import User

class UserCreate(BaseModel):
    """A user creation model."""
    email: EmailStr
    password: str
    name: str

    @field_validator("password")
    @classmethod
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
    
    class Config:
        from_attributes = True

class UserViewAdmin(BaseModel):
    """A user view model for administrators."""
    id: int
    email: EmailStr
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserViewPublic(BaseModel):
    """A user view model for the public."""
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """A user update model."""
    email: EmailStr|None = None
    name: str|None = None
    password: str|None = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str|None) -> str|None:
        """
        Validate the password.
        Requirements:
            - At least 8 characters long
            - At least one uppercase letter
            - At least one lowercase letter
            - At least one digit
            - At least one special character
        """
        if password is None:
            return None
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

    class Config:
        from_attributes = True

User_Pydantic = pydantic_model_creator(User, name="User", exclude=("id","password", "created_at", "updated_at"))
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
UserViewAdmin_Pydantic = pydantic_model_creator(User, name="UserViewAdmin")
UserViewPublic_Pydantic = pydantic_model_creator(User, name="UserViewPublic", exclude=("password",))
