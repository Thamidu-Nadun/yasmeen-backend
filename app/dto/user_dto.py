from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    id: int
    username: str
    email: EmailStr
    password_hash: str
    created_at: str


class UserCreateDTO(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str
