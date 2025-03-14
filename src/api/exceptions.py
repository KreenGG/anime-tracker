from fastapi import HTTPException, status

BadRequest = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad request",
)

UnauthorizedError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
)

NotFoundError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Content not found",
)
