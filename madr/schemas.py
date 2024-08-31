from pydantic import BaseModel, ConfigDict, EmailStr, BeforeValidator, validator
import re


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class AuthorSchema(BaseModel):
    name: str

    @validator('name')
    def sanitize_string(cls, v):
        # Remove todos os espaços em branco do início e do final
        v = v.strip()
        # Remove interrogação e exclamação
        v = re.sub(r'[?!]', '', v)
        # Substitui todas as ocorrências de um ou mais espaços por um único espaço
        v = re.sub(r'\s+', ' ', v)

        return v.lower()


class AuthorPublic(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class AuthorList(BaseModel):
    authors: list[AuthorSchema]


class BookSchema(BaseModel):
    title: str
    year: int
    author_id: int


class BookPublic(BaseModel):
    id: int
    title: str
    year: int
    author_id: int
    model_config = ConfigDict(from_attributes=True)


class BookList(BaseModel):
    books: list[BookSchema]
