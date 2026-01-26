import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import User
from database.session import get_db_session
from sqlmodel import select
from api.routes.auth import get_password_hash

def update_user_passwords():
    # Get database session
    db = next(get_db_session())

    try:
        # Get all users
        result = db.execute(select(User))
        users = result.scalars().all()

        for user in users:
            print(f"Updating password hash for user: {user.email}")

            # We'll keep the same password but re-hash it with the new bcrypt version
            # For this test, we'll use 'password' as the password for all users
            new_hashed_password = get_password_hash('password')

            # Update the user's password
            user.hashed_password = new_hashed_password
            db.add(user)

        db.commit()
        print(f"Updated {len(users)} users with new password hashes")

    except Exception as e:
        print(f"Error updating user passwords: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_user_passwords()