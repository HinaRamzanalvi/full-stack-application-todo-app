from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, SQLModel
from models.user import User, UserCreate, UserRead, UserLogin
from database.session import get_db_session
from middleware.auth import create_access_token
from models.user import pwd_context
from typing import Optional


router = APIRouter()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/auth/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db_session)):
    # Check if user already exists
    existing_user = db.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create the new user
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Define response model for login
class LoginResponse(SQLModel):
    access_token: str
    token_type: str
    user: UserRead


@router.post("/auth/login", response_model=LoginResponse)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db_session)):
    try:
        # Find the user by email
        statement = select(User).where(User.email == user_credentials.email)
        user = db.exec(statement).first()

        if not user:
            print(f"Login failed: User with email {user_credentials.email} not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify password using bcrypt
        is_password_valid = verify_password(user_credentials.password, user.hashed_password)
        print(f"Login attempt: email={user_credentials.email}, user_found={user is not None}, password_match={is_password_valid}")

        if not is_password_valid:
            print(f"Login failed: Invalid password for user {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create and return access token
        access_token = create_access_token(data={"sub": user.id})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "created_at": user.created_at
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions to maintain proper status codes
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )