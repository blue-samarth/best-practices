from repositories import create_user, get_user_by_email, get_user_by_id, get_all_users, update_user, delete_user
from schemas import UserCreate, UserUpdate, UserViewAdmin, UserViewPublic
from utils.passwords_handling import PasswordHandle
from utils.authToken import Token
# Here we will handle all the business logic related to the user entity.

async def register_user(email: str, name: str, password: str) -> UserViewPublic:
    """Register a new user."""
    user = await get_user_by_email(email)
    if user:
        raise ValueError("User already exists.")
    hashed_password = PasswordHandle.get_password_hash(password)
    user = await create_user(email, hashed_password, name)
    return UserViewPublic.model_validate(user)

async def login_user(email: str, password: str) -> dict:
    """Login a user."""
    user = await get_user_by_email(email)
    if not user:
        raise ValueError("User not found.")
    if not PasswordHandle.verify_password(password, user.password):
        raise ValueError("Incorrect password.")
    token = Token(user.id, 'user').create_token()
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
    }

async def change_user_password(user_id: int, old_password: str, new_password: str) -> UserViewPublic:
    """Change user password."""
    user = await get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found.")
    if not PasswordHandle.verify_password(old_password, user.password):
        raise ValueError("Incorrect password.")
    hashed_password = PasswordHandle.get_password_hash(new_password)
    user = await update_user(user_id, password=hashed_password)
    return UserViewPublic.model_validate(user)

async def list_all_users() -> list[UserViewAdmin]:
    """List all users."""
    users = await get_all_users()
    return [UserViewAdmin.model_validate(user) for user in users]

async def get_user(user_id: int) -> UserViewAdmin:
    """Get a user."""
    user = await get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found.")
    return UserViewAdmin.model_validate(user)

async def remove_user(user_id: int) -> bool:
    """Remove a user."""
    user = await get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found.")
    return await delete_user(user_id)
