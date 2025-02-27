from datetime import datetime

from tortoise.models import Model
from tortoise import fields

class User(Model):
    """A user model."""
    id: int = fields.IntField(pk=True)
    email: str = fields.CharField(max_length=50, unique=True)
    password: str = fields.CharField(max_length=255)
    name: str = fields.CharField(max_length=50)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.email})"

    class Meta:
        table = "users"