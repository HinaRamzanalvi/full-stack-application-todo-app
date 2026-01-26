import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import User, UserCreate
from database.session import get_db_session
from sqlmodel import Session
from api.routes.auth import get_password_hash, verify_password
from sqlmodel import select

def create_princess_user():
    # Create a new user
    email = "princess4177812@gmail.com"
    password = "password"  # You can change this to whatever you want
    name = "Princess User"

    # Get database session
    db = next(get_db_session())

    try:
        # Check if user already exists
        result = db.execute(select(User).where(User.email == email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            print(f"User with email {email} already exists!")
            print(f"User ID: {existing_user.id}")
            return

        # Hash the password using the same method as in auth.py
        hashed_password = get_password_hash(password)

        # Create the new user
        db_user = User(
            email=email,
            name=name,
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
    create_princess_user()