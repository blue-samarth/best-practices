# Here we will handle all the database operations related to the user entity.
from src.models.users import User


async def create_user(email: str, hashed_password: str, name: str) -> User:
    """Create a new user with a hashed password."""
    try:
        return await User.create(email=email, password=hashed_password, name=name)
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise Exception(str(e))

async def get_user_by_email(email: str) -> User | None:
    """Retrieve a user by email."""
    try:
        return await User.filter(email=email).first()
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise Exception(str(e))

async def get_user_by_id(user_id: int) -> User | None:
    """Retrieve a user by ID."""
    try:
        return await User.filter(id=user_id).first()
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise Exception(str(e))

async def get_all_users() -> list[User]:
    """Retrieve all users."""
    try:
        return await User.all()
    except Exception as e:
        raise Exception(str(e))

async def update_user(user_id: int, **kwargs) -> User | None:
    """Update a user."""
    user = await User.filter(id=user_id).first()
    if user:
        await user.update_from_dict(kwargs).save()
    else: 
        return None
    return user

async def delete_user(user_id: int) -> bool:
    """Delete a user."""
    try:
        deleted_count = await User.filter(id=user_id).delete()
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise Exception(str(e))
    return deleted_count > 0
