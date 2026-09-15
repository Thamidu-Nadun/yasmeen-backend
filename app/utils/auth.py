from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required


def auth(fn):

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        jwt_key = get_jwt_identity()
        if not jwt_key:
            return {"error": "User not authenticated"}, 401

        return fn(*args, **kwargs)

    return wrapper
