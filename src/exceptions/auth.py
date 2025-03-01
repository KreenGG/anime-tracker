class AuthError(Exception):
    detail: str

class UserAlreadyExistsError(AuthError):
    detail = "User already exists"

class InvalidCredentialsError(AuthError):
    detail = "Invalid credentials"
