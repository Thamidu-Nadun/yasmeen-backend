from app.models.User import User, db
from datetime import datetime


def get_user(email: str) -> User:
    """Retrieve a user record by email.
    Args:
        email (str): The email of the user to retrieve.
    Returns:
        User: The User object with the specified email, or None if not found.
    """
    return User.query.filter_by(email=email).first()


def create_user(username: str, email: str, password_hash: str) -> User:
    """Create a new user record in the database with default values.
    Returns:
        User: The created User object.
    """
    if exist_user := get_user(email):
        return None  # User already exists, return None or handle as needed
    new_user = User(
        username=username,
        email=email,
        password=password_hash,
        created_at=datetime.now(),
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user


def delete_user(user_id: int) -> bool:
    """Delete a user record by its ID.
    Args:
        user_id (int): The ID of the user to delete.
    Returns:
        bool: True if the user was deleted, False if not found.
    """
    if user := User.query.get(user_id):
        db.session.delete(user)
        db.session.commit()
        return True
    return False
