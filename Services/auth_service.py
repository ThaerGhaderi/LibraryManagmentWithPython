import logging

from Models.user import User, UserRole
from auth.exceptions import (
    InvalidCredentialsError,
    PermissionDeniedError,
    UsernameAlreadyExistsError,
)
from auth.password_hasher import PasswordHasher
from auth.session import Session
from repositories.user_repository import UserRepository


logger = logging.getLogger(__name__)


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository | None = None,
        session: Session | None = None,
    ) -> None:
        self.user_repository = (
            user_repository
            if user_repository is not None
            else UserRepository()
        )
        self.session = session if session is not None else Session()

    def register(
        self,
        full_name: str,
        username: str,
        password: str,
    ) -> User:
        full_name = full_name.strip()
        username = username.strip().lower()

        if not full_name:
            logger.warning("Registration failed: empty full name")
            raise ValueError("Full name cannot be empty.")

        if not username:
            logger.warning("Registration failed: empty username")
            raise ValueError("Username cannot be empty.")

        existing_user = self.user_repository.find_by_username(username)

        if existing_user is not None:
            logger.warning(
                "Registration failed for username=%s: username already exists",
                username,
            )
            raise UsernameAlreadyExistsError(
                f"Username '{username}' already exists."
            )

        PasswordHasher.validate_password(password)
        password_hash, salt = PasswordHasher.hash_password(password)

        users = self.user_repository.get_all()
        role = UserRole.LIBRARIAN if not users else UserRole.MEMBER

        user = User(
            full_name=full_name,
            username=username,
            password_hash=password_hash,
            salt=salt,
            role=role,
        )

        users.append(user)
        self.user_repository.save_all(users)
        self.session.login(user)

        logger.info(
            "User registered: id=%s username=%s role=%s",
            user.id_user,
            user.username,
            user.role.value,
        )

        return user

    def login(
        self,
        username: str,
        password: str,
    ) -> User:
        username = username.lower().strip()
        user = self.user_repository.find_by_username(username)

        if user is None:
            logger.warning(
                "Failed login attempt for username=%s",
                username,
            )
            raise InvalidCredentialsError(
                "Invalid username or password."
            )

        if not user.active:
            logger.warning(
                "Failed login attempt for username=%s: inactive account",
                username,
            )
            raise InvalidCredentialsError(
                "This account is inactive."
            )

        valid = PasswordHasher.verify_password(
            password,
            user.password_hash,
            user.salt,
        )

        if not valid:
            logger.warning(
                "Failed login attempt for username=%s",
                username,
            )
            raise InvalidCredentialsError(
                "Invalid username or password."
            )

        self.session.login(user)

        logger.info(
            "User logged in: id=%s username=%s",
            user.id_user,
            user.username,
        )

        return user

    def logout(self) -> None:
        current_user = self.session.current_user
        self.session.logout()

        if current_user is not None:
            logger.info(
                "User logged out: id=%s username=%s",
                current_user.id_user,
                current_user.username,
            )
        else:
            logger.info("User logged out")

    def get_current_user(self) -> User:
        return self.session.require_authentication()

    def require_librarian(self) -> User:
        user = self.session.require_authentication()

        if user.role != UserRole.LIBRARIAN:
            logger.warning(
                "Permission denied for user id=%s username=%s: librarian access required",
                user.id_user,
                user.username,
            )
            raise PermissionDeniedError(
                "Librarian permission required."
            )

        return user

    def is_authenticated(self) -> bool:
        return self.session.is_authenticated
