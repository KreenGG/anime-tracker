from pydantic import BaseModel, EmailStr, Field


class UserGet(BaseModel):
    id: int
    email: EmailStr
    nickname: str

    class Config:
        from_attributes = True


class UserDTO(UserGet):
    hashed_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserLogin):
    nickname: str = Field(min_length=3, max_length=32)
