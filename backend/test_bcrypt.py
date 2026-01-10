import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import pwd_context

def test_password_verification():
    # Test password verification directly
    plain_password = "password"
    hashed_password = "$2b$12$mPGaBALr0F5k5..."  # This is just the start, we need the full hash

    # Let's create a new hash and test verification
    new_hash = pwd_context.hash("password")
    print(f"New hash: {new_hash}")

    # Test verification
    is_valid = pwd_context.verify("password", new_hash)
    print(f"Verification result: {is_valid}")

    # Test with wrong password
    is_invalid = pwd_context.verify("wrongpassword", new_hash)
    print(f"Wrong password verification: {is_invalid}")

if __name__ == "__main__":
    test_password_verification()