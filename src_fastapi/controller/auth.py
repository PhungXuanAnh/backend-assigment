import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()


AUTH_USERS = [
    {"username": "admin", "password": "admin", "company": "", "is_superuser": True},
    {
        "username": "department_manager_company_99",
        "password": "1234",
        "company": "company-99",
        "is_superuser": False,
    },
]


def get_auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")

    for auth_user in AUTH_USERS:
        correct_username_bytes = auth_user["username"].encode("utf8")
        is_correct_username = secrets.compare_digest(current_username_bytes, correct_username_bytes)

        correct_password_bytes = auth_user["password"].encode("utf8")
        is_correct_password = secrets.compare_digest(current_password_bytes, correct_password_bytes)

        if is_correct_username and is_correct_password:
            return auth_user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
