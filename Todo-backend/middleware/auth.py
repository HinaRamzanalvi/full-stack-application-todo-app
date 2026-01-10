from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from database.config import settings

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 30 days
        expire = datetime.utcnow() + timedelta(days=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.better_auth_secret, algorithm="HS256")
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """Verify JWT token and return user data"""
    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
        return TokenData(user_id=user_id)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Get current authenticated user from JWT token"""
    token_data = verify_token(credentials.credentials)
    return token_data


# Alias for compatibility
current_user = get_current_user