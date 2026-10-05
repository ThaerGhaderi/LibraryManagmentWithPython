import logging

from Models.user import User
from auth.exceptions import NotAuthenticatedError
from auth.password_hasher import PasswordHasher
from auth.session import Session
from repositories.user_repository import UserRepository


logger = logging.getLogger(__name__)


class UserService:
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

  

    def get_current_user(self) -> User:
        return self.session.require_authentication()


    def update_full_name(
        self,
        full_name: str,
    ) -> User:
        current_user = self.get_current_user()
        full_name = full_name.strip()

        if not full_name:
            logger.warning(
                "Full name update failed for user id=%s username=%s: empty full name",
                current_user.id_user,
                current_user.username,
            )
            raise ValueError("Full name cannot be empty.")

        users = self.user_repository.get_all()
        stored_user = self._find_user_by_id(
            users,
            current_user.id_user,
        )

        if stored_user is None:
            logger.warning(
                "Full name update failed for user id=%s username=%s: user not found",
                current_user.id_user,
                current_user.username,
            )
            raise NotAuthenticatedError(
                "Current user was not found."
            )

        old_full_name = stored_user.full_name
        stored_user.update_full_name(full_name)
        self.user_repository.save_all(users)

        # Keep Session synchronized with the saved user.
        self.session.login(stored_user)

        logger.info(
            "User full name updated: id=%s username=%s old_full_name=%s new_full_name=%s",
            stored_user.id_user,
            stored_user.username,
            old_full_name,
            stored_user.full_name,
        )

        return stored_user


    def change_password(
        self,
        current_password: str,
        new_password: str,
        confirm_password: str,
    ) -> None:
        current_user = self.get_current_user()

        if not PasswordHasher.verify_password(
            current_password,
            current_user.password_hash,
            current_user.salt,
        ):
            logger.warning(
                "Password change failed for user id=%s username=%s: current password mismatch",
                current_user.id_user,
                current_user.username,
            )
            raise ValueError("Current password is incorrect.")

        if new_password != confirm_password:
            logger.warning(
                "Password change failed for user id=%s username=%s: password confirmation mismatch",
                current_user.id_user,
                current_user.username,
            )
            raise ValueError("New passwords do not match.")

        PasswordHasher.validate_password(new_password)
        new_hash, new_salt = PasswordHasher.hash_password(new_password)

        users = self.user_repository.get_all()
        stored_user = self._find_user_by_id(
            users,
            current_user.id_user,
        )

        if stored_user is None:
            logger.warning(
                "Password change failed for user id=%s username=%s: user not found",
                current_user.id_user,
                current_user.username,
            )
            raise NotAuthenticatedError(
                "Current user was not found."
            )

        stored_user.update_password(
            new_hash,
            new_salt,
        )
        self.user_repository.save_all(users)

        self.session.login(stored_user)

        logger.info(
            "Password changed for user: id=%s username=%s",
            stored_user.id_user,
            stored_user.username,
        )

 
    @staticmethod
    def _find_user_by_id(
        users: list[User],
        user_id: int,
    ) -> User | None:
        for user in users:
            if user.id_user == user_id:
                return user

        return None
