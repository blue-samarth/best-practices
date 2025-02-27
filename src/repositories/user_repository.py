# Here we will handle all the database operations related to the user entity.
from src.models.users import User


class UserRepository:
    """A class to handle the user repository."""

    @staticmethod
    async def create_user(email: str, hashed_password: str, name: str) -> User:
        """Create a new user with a hashed password."""
        return await User.create(email=email, password=hashed_password, name=name)

    @staticmethod
    async def get_user_by_email(email: str) -> User | None:
        """Retrieve a user by email."""
        return await User.filter(email=email).first()

    @staticmethod
    async def get_user_by_id(user_id: int) -> User | None:
        """Retrieve a user by ID."""
        return await User.filter(id=user_id).first()

    @staticmethod
    async def get_all_users() -> list[User]:
        """Retrieve all users."""
        return await User.all()

    @staticmethod
    async def update_user(user_id: int, **kwargs) -> User | None:
        """Update a user."""
        user = await User.filter(id=user_id).first()
        if user:
            await user.update_from_dict(kwargs).save()
        return user

    @staticmethod
    async def delete_user(user_id: int) -> bool:
        """Delete a user."""
        deleted_count = await User.filter(id=user_id).delete()
        return deleted_count > 0
    