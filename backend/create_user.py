import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import User, UserCreate
from database.session import get_db
from sqlmodel import Session, select
from api.routes.auth import get_password_hash, verify_password

def create_test_user():
    # Create a new user
    email = "test@example.com"
    password = "password"
    name = "Test User"

    # Create the user object
    user_create = UserCreate(email=email, password=password, name=name)

    # Get database session
    db = next(get_db())

    try:
        # Check if user already exists
        result = db.execute(select(User).where(User.email == email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            print(f"User with email {email} already exists!")
            return

        # Hash the password using the same method as in auth.py
        hashed_password = get_password_hash(password)

        # Create the new user
        db_user = User(
            email=user_create.email,
            name=user_create.name,
            hashed_password=hashed_password
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        print(f"User created successfully!")
        print(f"Email: {db_user.email}")
        print(f"Password: {password}")
        print(f"User ID: {db_user.id}")

    except Exception as e:
        print(f"Error creating user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()