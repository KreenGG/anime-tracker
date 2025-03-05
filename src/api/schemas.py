from typing import Generic, TypeVar

from pydantic import BaseModel, Field

ResponseType = TypeVar("ResponseType")


class ApiResponse(BaseModel, Generic[ResponseType]):
    data: ResponseType | None = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    detail: str
