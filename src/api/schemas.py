from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

ResponseType = TypeVar("ResponseType")


class ApiResponse(BaseModel, Generic[ResponseType]):
    data: ResponseType | dict[str, Any] | None = Field(default_factory=dict[str, Any])


class ErrorResponse(BaseModel):
    detail: str
