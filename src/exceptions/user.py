class UserError(Exception):
    detail: str

class UserAlreadyExistsError(UserError):
    detail = "User already exists"

class InvalidCredentialsError(UserError):
    detail = "Invalid credentials"
