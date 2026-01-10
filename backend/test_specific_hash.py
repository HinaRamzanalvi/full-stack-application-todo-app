import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import pwd_context

def test_specific_hash():
    # Test the specific hash from the database
    stored_hash = "$2b$12$mPGaBALr0F5k5gOnUNEYLu5/PanC0vuFtI4j3NV8ke9nn6GORg/92"
    correct_password = "password"
    wrong_password = "wrongpassword"

    print(f"Testing hash: {stored_hash}")

    # Test with correct password
    is_valid = pwd_context.verify(correct_password, stored_hash)
    print(f"Correct password ('password') verification: {is_valid}")

    # Test with wrong password
    is_invalid = pwd_context.verify(wrong_password, stored_hash)
    print(f"Wrong password ('wrongpassword') verification: {is_invalid}")

    # Test another variation
    is_invalid2 = pwd_context.verify("Password", stored_hash)  # Capital P
    print(f"Different case ('Password') verification: {is_invalid2}")

if __name__ == "__main__":
    test_specific_hash()