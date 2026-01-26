import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import pwd_context, User
from database.session import get_db_session
from sqlmodel import select
from api.routes.auth import verify_password

def test_login_flow():
    # Simulate the exact login flow
    email = "princess4177812@gmail.com"
    password = "password"  # This should work based on our hash test

    # Get database session
    db = next(get_db_session())

    try:
        # Find the user by email (like in auth.py line 59)
        from sqlmodel import select
        statement = select(User).where(User.email == email)
        result = db.execute(statement)
        user = result.scalar_one_or_none()

        print(f"User found: {user is not None}")
        if user:
            print(f"User email: {user.email}")
            print(f"Stored hash: {user.hashed_password}")

            # Verify password (like in auth.py line 71)
            is_password_valid = verify_password(password, user.hashed_password)
            print(f"Password verification result: {is_password_valid}")

            # Test directly with pwd_context
            direct_verify = pwd_context.verify(password, user.hashed_password)
            print(f"Direct verification result: {direct_verify}")

    finally:
        db.close()

if __name__ == "__main__":
    test_login_flow()