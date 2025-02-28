from fastapi import APIRouter, Depends, HTTPException
from src.services import user_service

router = APIRouter()

@router.post("/register")
async def register_user(email: str, name: str, password: str):
    """Register a new user."""
    try:
        new_user = await user_service.register_user(email, name, password)
        return {
            "status": "success",
            "status_code": 201,
            "data": new_user
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login_user(email: str, password: str):
    """Login a user."""
    try:
        user_token = await user_service.login_user(email, password)
        return {
            "status": "success",
            "status_code": 200,
            "data": user_token
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/change-password")
async def change_user_password(user_id: int, old_password: str, new_password: str):
    """Change user password."""
    try:
        updated_user = await user_service.change_user_password(user_id, old_password, new_password)
        return {
            "status": "success",
            "status_code": 200,
            "data": updated_user
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/users")
async def list_all_users():
    """List all users."""
    try:
        users = await user_service.list_all_users()
        return {
            "status": "success",
            "status_code": 200,
            "data": users
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}")
async def get_user(user_id: int):
    """Get a user."""
    try:
        user = await user_service.get_user(user_id)
        return {
            "status": "success",
            "status_code": 200,
            "data": user
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/user/{user_id}")
async def remove_user(user_id: int):
    """Remove a user."""
    try:
        is_deleted = await user_service.remove_user(user_id)
        if not is_deleted:
            raise HTTPException(status_code=404, detail="User not found.")
        return {
            "status": "success",
            "status_code": 204,
            "data": None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
