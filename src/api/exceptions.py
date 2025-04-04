from fastapi import HTTPException, status

# ? Возможно стоит от них избавиться
BadRequest = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=[{"msg": "Bad request"}],
)

NotFoundError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=[{"msg": "Content not found"}],
)
