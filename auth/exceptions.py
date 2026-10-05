

class AuthError(Exception):
    """Base class for authentication errors."""
    pass


class InvalidCredentialsError(AuthError):
    """Raised when the provided credentials are invalid."""
    pass

class UsernameAlreadyExistsError(AuthError):
    """Raised when the username already exists in the system."""
    pass


class WeakPasswordError(AuthError):
    """Raised when the provided password is considered weak."""
    pass

class NotAuthenticatedError(AuthError):
    """Raised when a user tries to access a resource without being authenticated."""
    pass

class PermissionDeniedError(AuthError):
    """Raised when a user tries to access a resource they don't have permission for."""
    pass