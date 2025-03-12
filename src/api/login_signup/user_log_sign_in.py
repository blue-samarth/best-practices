# This file contains the routes for the user login and signup.
from fastapi import APIRouter, HTTPException, Body

from src.schema.user_schema import UserCreate, UserLogin, PasswordChange, GetUserID, UserUpdate
from src.services import user_service
from src.utils.decorators import requires_auth
from src.utils.responses import APIResponse

router = APIRouter()

@router.post("/register", response_model=APIResponse)
async def register_user(user_data: UserCreate):
    """Register a new user."""
    try:
        new_user = await user_service.register_user(user_data)
        new_user = new_user.model_dump()
        return APIResponse.respond(
            status_code=201,
            data=new_user,
            message="User registered successfully.",
            status="success"
        )
    except ValueError as e:
        return APIResponse.respond(
            status_code=400,
            message=str(e),
            status="There was an error registering the user."
        )
    except Exception as e:
        return APIResponse.respond(
            status_code=500,
            message=str(e),
            status="error"
        )

@router.post("/login", response_model=APIResponse)
async def login_user(credentials: UserLogin) -> APIResponse:
    """Login a user."""
    try:
        user_token = await user_service.login_user(credentials.email, credentials.password)
        return APIResponse.respond(
            status_code=200,
            data=user_token,
            message="User logged in successfully.",
            status="success"
        )
    except ValueError as e:
        return APIResponse.respond(
            status_code=400,
            message=str(e),
            status="The username or password is incorrect."
        )
    except Exception as e:
        return APIResponse.respond(
            status_code=500,
            message=str(e),
            status="There was an error logging in."
        )

@router.post("/change-password")
@requires_auth(["admin", "user"])
async def change_user_password(password_data: PasswordChange,
                               token_user_id: int|None = None,
                               token_role: str|None = None):
    """
    Route to change the user password.
    Args:
        user_id (int): The user id.
        old_password (str): The old password.
        new_password (str): The new password.
        token_user_id (int): The user id from the token provided via the decorator.
    Returns:
        dict: The response.
    Raises:
        HTTPException(400): If the user is not found or the password is incorrect.
        HTTPException(403): If the user does not have the necessary permissions.
        HTTPException(500): If there is an internal server error.
    """
    try:
        if token_role == 'user' and password_data.user_id != token_user_id:
            raise HTTPException(status_code=403, detail="Insufficient permissions.")
        updated_user = await user_service.change_user_password(
            password_data.user_id,
            password_data.old_password,
            password_data.new_password
        )
        return APIResponse.respond(
            status_code=200,
            data=updated_user,
            message="Password changed successfully.",
            status="success"
        )
    except ValueError as e:
        return APIResponse.respond(
            status_code=400,
            message=str(e),
            status="The password is incorrect."
        )
    except Exception as e:
        return APIResponse.respond(
            status_code=500,
            message=str(e),
            status="There was an error changing the password."
        )
    
@requires_auth(["admin", "user"])
@router.put("/user", response_model=APIResponse)
async def update_user(user_data: UserUpdate, 
                      token_user_id: int, token_role: str):
    """
    Update user details.
    Args:
        user_id (int): The user id.
        user_to_update (dict): The user details to update.
        token_user_id (int): The user id from the token.
        token_role (str): The role from the token.
    Returns:
        dict: The response.
    Raises:
        HTTPException(400): If the user is not found.
        HTTPException(403): If the user does not have the necessary permissions.
        HTTPException(500): If there is an internal server error.
    """
    try:
        if token_role == "admin":
            updated_user = await user_service.update_user_details(user_data.user_id, user_data.dict(exclude_unset=True), is_admin=True)
        else:
            if user_data.user_id != token_user_id:
                raise HTTPException(status_code=403, detail="Insufficient permissions.")
            updated_user = await user_service.update_user_details(user_data.user_id, user_data.dict(exclude_unset=True), is_admin=False)

        return APIResponse.respond(
            status_code=200,
            data=updated_user,
            message="User updated successfully.",
            status="success"
        )
    except ValueError as e:
        return APIResponse.respond(
            status_code=400,
            message=str(e),
            status="The user was not found."
        )
    except Exception as e:
        return APIResponse.respond(
            status_code=500,
            message=str(e),
            status="There was an error updating the user."
        )

@requires_auth(["admin"])
@router.get("/users", response_model=APIResponse)
async def list_all_users():
    """List all users."""
    try:
        users = await user_service.list_all_users()
        return APIResponse.respond(
            status_code=200,
            data=users,
            message="Users retrieved successfully.",
            status="success"
        )
    except ValueError as e:
        return APIResponse.respond(
            status_code=400,
            message=str(e),
            status="There was an error retrieving the users."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user", response_model=APIResponse)
async def get_user(user_data: GetUserID = Body(...)):
    """Get a user."""
    try:
        user = await user_service.get_user(user_data.user_id)
        return APIResponse.respond(
            status_code=200,
            data=user,
            message="User retrieved successfully.",
            status="success"
        )
    except ValueError as e:
        return APIResponse.respond(
            status_code=400,
            message=str(e),
            status="The user was not found."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@requires_auth(["admin", "user"])
@router.delete("/user", response_model=APIResponse)
async def remove_user(token_user_id: int, token_role: str, user_data: GetUserID = Body(...)):
    """
    Remove a user.
    Args:
        user_id (int): The user id.
        token_user_id (int): The user id from the token.
        token_role (str): The role from the token.
    returns:
        dict: The response:
            204: If the user is removed successfully.
            404: If the user is not found.
    Raises:
        HTTPException(403): If the user does not have the necessary permissions.
        HTTPException(500): If there is an internal server error.
    """
    try:
        if token_role == "user" and user_data.user_id != token_user_id:
            # raise HTTPException(status_code=403, detail="Insufficient permissions.")
            return APIResponse.respond(
                status_code=403,
                message="Insufficient permissions.",
                status="error"
            )
        is_deleted = await user_service.remove_user(user_data.user_id)
        if not is_deleted:
            raise HTTPException(status_code=404, detail="User not found.")
        return APIResponse.respond(
            status_code=204,
            message="User removed successfully.",
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
