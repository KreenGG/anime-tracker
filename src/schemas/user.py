from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(UserLogin):
    ...

class UserGet(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
