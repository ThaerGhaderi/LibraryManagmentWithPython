import logging

from Models.borrowing import BorrowingStatus
from Models.user import User, UserRole
from auth.session import Session
from repositories.borrowing_repository import BorrowingRepository
from repositories.user_repository import UserRepository


logger = logging.getLogger(__name__)


class MemberError(Exception):
    pass


class MemberNotFoundError(MemberError):
    pass


class MemberPermissionError(MemberError):
    pass


class MemberHasActiveBorrowingsError(MemberError):
    pass


class MemberService:
    def __init__(
        self,
        session: Session,
        user_repository: UserRepository,
        borrowing_repository: BorrowingRepository,
    ) -> None:
        self.session = session
        self.user_repository = user_repository
        self.borrowing_repository = borrowing_repository

    def get_all_members(self) -> list[User]:
        self._require_librarian()

        users = self.user_repository.get_all()
        members = [
            user
            for user in users
            if user.role == UserRole.MEMBER
        ]

        logger.info("Fetched members: count=%s", len(members))
        return members

    def search_members(
        self,
        query: str,
    ) -> list[User]:
        self._require_librarian()
        query = query.strip().lower()

        if not query:
            logger.warning("Member search skipped: empty query")
            return []

        members = self.get_all_members()
        results = [
            member
            for member in members
            if (
                query in member.full_name.lower()
                or query in member.username.lower()
            )
        ]

        logger.info(
            "Members searched: query=%s results=%s",
            query,
            len(results),
        )
        return results

    def get_member_by_id(
        self,
        user_id: int,
    ) -> User:
        self._require_librarian()

        member = self.user_repository.find_by_id(user_id)

        if member is None or member.role != UserRole.MEMBER:
            logger.warning("Member not found by id=%s", user_id)
            raise MemberNotFoundError(
                f"Member with ID {user_id} was not found."
            )

        logger.info(
            "Member found: id=%s username=%s",
            member.id_user,
            member.username,
        )
        return member

    def get_member_borrowings(
        self,
        user_id: int,
    ):
        self._require_librarian()

        member = self.get_member_by_id(user_id)
        borrowings = self.borrowing_repository.get_all()
        results = [
            borrowing
            for borrowing in borrowings
            if borrowing.user_id == member.id_user
        ]

        logger.info(
            "Fetched member borrowings: member_id=%s count=%s",
            member.id_user,
            len(results),
        )
        return results

    def deactivate_member(
        self,
        user_id: int,
    ) -> None:
        self._require_librarian()
        member = self.get_member_by_id(user_id)

        if not member.active:
            logger.warning(
                "Deactivate member skipped: already inactive user_id=%s",
                user_id,
            )
            raise MemberError("Member is already inactive.")

        borrowings = self.borrowing_repository.get_all()
        has_active_borrowings = any(
            borrowing.user_id == member.id_user
            and borrowing.status == BorrowingStatus.ACTIVE
            for borrowing in borrowings
        )

        if has_active_borrowings:
            logger.warning(
                "Deactivate member failed: active borrowings user_id=%s username=%s",
                member.id_user,
                member.username,
            )
            raise MemberHasActiveBorrowingsError(
                "Cannot deactivate a member "
                "with active borrowings."
            )

        users = self.user_repository.get_all()
        stored_member = self._find_in_list(
            users,
            member.id_user,
        )

        if stored_member is None:
            logger.warning("Deactivate member failed: member not found id=%s", user_id)
            raise MemberNotFoundError(
                f"Member with ID {user_id} was not found."
            )

        stored_member.deactivate()
        self.user_repository.save_all(users)

        logger.info(
            "Member deactivated: id=%s username=%s",
            stored_member.id_user,
            stored_member.username,
        )

    def activate_member(
        self,
        user_id: int,
    ) -> None:
        self._require_librarian()
        member = self.get_member_by_id(user_id)

        if member.active:
            logger.warning(
                "Activate member skipped: already active user_id=%s",
                user_id,
            )
            raise MemberError("Member is already active.")

        users = self.user_repository.get_all()
        stored_member = self._find_in_list(
            users,
            member.id_user,
        )

        if stored_member is None:
            logger.warning("Activate member failed: member not found id=%s", user_id)
            raise MemberNotFoundError(
                f"Member with ID {user_id} was not found."
            )

        stored_member.activate()
        self.user_repository.save_all(users)

        logger.info(
            "Member activated: id=%s username=%s",
            stored_member.id_user,
            stored_member.username,
        )

    def _require_librarian(self) -> None:
        user = self.session.require_authentication()

        if user.role != UserRole.LIBRARIAN:
            logger.warning(
                "Permission denied for user id=%s username=%s: librarian access required for member operations",
                user.id_user,
                user.username,
            )
            raise MemberPermissionError(
                "Only librarians can manage members."
            )

    @staticmethod
    def _find_in_list(
        users: list[User],
        user_id: int,
    ) -> User | None:
        for user in users:
            if user.id_user == user_id:
                return user

        return None
