from devtrack.core.security import (
    hash_password, verify_password, create_access_token, decode_access_token
)

def test_hash_password_produces_different_string():
    hashed = hash_password("mypassword")
    assert hashed != "mypassword"

def test_verify_password_correct():
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed) is True

def test_verify_password_incorrect():
    hashed = hash_password("mypassword")
    assert verify_password("wrongpassword", hashed) is False

def test_token_roundtrip():
    token = create_access_token({"user_id": 7})
    payload = decode_access_token(token)
    assert payload["user_id"] == 7