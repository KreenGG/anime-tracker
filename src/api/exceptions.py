from fastapi import HTTPException, status

BadRequest = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad request",
)

NotFoundError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Content not found",
)
