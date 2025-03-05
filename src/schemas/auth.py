from pydantic import BaseModel


class TokenPayload(BaseModel):
    user_id: int


class Token(BaseModel):
    access_token: str
    token_type: str
