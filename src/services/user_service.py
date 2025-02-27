from repositories.user_repo import UserRepository
from utils.security import verify_password, create_access_token

async def login_user(email: str, password: str) -> dict:
    """Handle login logic: verify user, check password, generate token."""
    user = await UserRepository.get_user_by_email(email)
    if not user or not verify_password(password, user.password):
        return None  # Authentication failed

    token = create_access_token({"sub": user.email})  # Generate JWT token
    return {"access_token": token, "token_type": "bearer"}
