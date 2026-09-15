from app.repo.user_repo import get_user, create_user, delete_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.dto.user_dto import UserCreateDTO, UserLoginDTO
from flask_jwt_extended import create_access_token


def login_user(user: UserLoginDTO) -> dict:
    """Authenticate a user based on email and password.
    Args:
        user_login_dto (UserLoginDTO): The DTO containing the user's email and password.
    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    if exist_user := get_user(user.email):
        if not check_password_hash(exist_user.password, user.password):
            return {"error": "Invalid password"}
        else:
            token = create_access_token(identity=str(exist_user.id))
            return {"message": "Login successful", "access_token": token}
    else:
        return {"error": "User not found"}


def register_user(user: UserCreateDTO):
    """Register a new user in the system.
    Args:
        user_create_dto (UserCreateDTO): The DTO containing the user's registration details.
    Returns:
        User: The created User object.
    """
    password_hash = generate_password_hash(user.password)
    if not (new_user := create_user(user.username, user.email, password_hash)):
        return {"error": "User already exists"}
    return new_user
