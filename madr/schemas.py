from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    senha: str


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    senha: str
