from repositories import create_user, get_user_by_email, get_user_by_id, get_all_users, update_user, delete_user
from schemas import UserCreate, UserUpdate, UserViewAdmin, UserViewPublic
from utils.passwords_handling import PasswordHandle
# Here we will handle all the business logic related to the user entity.

async def create_new_user(user: UserCreate) -> UserViewAdmin:
    """Create a new user."""
    hashed_password = PasswordHandle.hash_password(user.password)
    new_user = await create_user(user.email, hashed_password, user.name)
    return UserViewAdmin.from_orm(new_user)

async def get_user(user_id: int) -> UserViewAdmin:
    """Retrieve a user."""
    user = await get_user_by_id(user_id)
    return UserViewAdmin.from_orm(user)