import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import jwt

# Import the decorator and token handler from your module.
# Adjust the import paths as necessary.
from src.utils.decorators import requires_auth, token_handler
from src.utils.authToken import InsufficientPermissionsError

# Create a simple FastAPI app with a dummy protected endpoint.
app = FastAPI()

@app.get("/protected")
@requires_auth(roles=["admin"])
async def protected_route(token_user_id: str|None = None, token_role: str|None = None):
    # The extra kwargs injected by the decorator (token_user_id, token_role) are used here.
    return {"user_id": token_user_id, "role": token_role}

client = TestClient(app)

def test_valid_token(monkeypatch):
    # Monkeypatch the token_handler.validate_token to simulate a valid token.
    def valid_token(token: str, roles: list):
        return {"user_id": "123", "role": "admin"}
    monkeypatch.setattr(token_handler, "validate_token", valid_token)
    
    response = client.get("/protected", headers={"Authorization": "Bearer validtoken"})
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "123"
    assert data["role"] == "admin"
