from app.user_authentication import hash_password, verify_password


def test_password():
    assert verify_password("asldmfo23#v*m", hash_password("asldmfo23#v*m"))
