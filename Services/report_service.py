import logging
from collections import Counter
from datetime import date

from Models.book import Book
from Models.borrowing import Borrowing, BorrowingStatus
from Models.user import User, UserRole
from auth.session import Session
from repositories.book_repository import BookRepository
from repositories.borrowing_repository import BorrowingRepository
from repositories.user_repository import UserRepository


logger = logging.getLogger(__name__)


class ReportError(Exception):
    """Base class for report-related operations."""


class ReportPermissionError(ReportError):
    """Raised when a non-librarian tries to access reports."""


class ReportService:
    TOP_RESULTS_LIMIT = 5

    def __init__(
        self,
        session: Session,
        book_repository: BookRepository,
        user_repository: UserRepository,
        borrowing_repository: BorrowingRepository,
    ) -> None:
        self.session = session
        self.book_repository = book_repository
        self.user_repository = user_repository
        self.borrowing_repository = borrowing_repository

    def generate_report(self) -> dict:
        self._require_librarian()

        books = self.book_repository.get_all()
        users = self.user_repository.get_all()
        borrowings = self.borrowing_repository.get_all()

        report = {
            "generated_at": date.today().isoformat(),
            "books": self._build_book_statistics(books),
            "users": self._build_user_statistics(users),
            "borrowings": self._build_borrowing_statistics(borrowings),
            "rankings": self._build_rankings(
                books,
                users,
                borrowings,
            ),
        }

        logger.info(
            "Report generated: books=%s users=%s borrowings=%s",
            len(books),
            len(users),
            len(borrowings),
        )
        return report

    @staticmethod
    def _build_book_statistics(
        books: list[Book],
    ) -> dict:
        total_books = len(books)
        available_books = sum(1 for book in books if book.available)
        borrowed_books = sum(1 for book in books if not book.available)

        return {
            "total": total_books,
            "available": available_books,
            "borrowed": borrowed_books,
        }

    @staticmethod
    def _build_user_statistics(
        users: list[User],
    ) -> dict:
        total_users = len(users)
        total_members = sum(1 for user in users if user.role == UserRole.MEMBER)
        total_librarians = sum(
            1 for user in users if user.role == UserRole.LIBRARIAN
        )

        return {
            "total": total_users,
            "members": total_members,
            "librarians": total_librarians,
        }

    @staticmethod
    def _build_borrowing_statistics(
        borrowings: list[Borrowing],
    ) -> dict:
        total_borrowings = len(borrowings)
        active_borrowings = [
            borrowing
            for borrowing in borrowings
            if borrowing.status == BorrowingStatus.ACTIVE
        ]
        returned_borrowings = [
            borrowing
            for borrowing in borrowings
            if borrowing.status == BorrowingStatus.RETURNED
        ]
        overdue_borrowings = [
            borrowing
            for borrowing in active_borrowings
            if borrowing.end_date < date.today()
        ]
        total_fines = sum(borrowing.fine for borrowing in borrowings)
        completed_durations = [
            borrowing.calculate_duration()
            for borrowing in returned_borrowings
            if borrowing.returned_at is not None
        ]
        average_duration = (
            sum(completed_durations) / len(completed_durations)
            if completed_durations
            else 0.0
        )

        return {
            "total": total_borrowings,
            "active": len(active_borrowings),
            "returned": len(returned_borrowings),
            "overdue": len(overdue_borrowings),
            "total_fines": total_fines,
            "average_duration": average_duration,
        }

    def _build_rankings(
        self,
        books: list[Book],
        users: list[User],
        borrowings: list[Borrowing],
    ) -> dict:
        book_lookup = {book.id_book: book for book in books}
        user_lookup = {user.id_user: user for user in users}
        book_counts = Counter(borrowing.book_id for borrowing in borrowings)
        user_counts = Counter(borrowing.user_id for borrowing in borrowings)

        most_borrowed_books = []
        for book_id, count in book_counts.most_common(self.TOP_RESULTS_LIMIT):
            book = book_lookup.get(book_id)
            if book is None:
                continue

            most_borrowed_books.append(
                {
                    "book_id": book.id_book,
                    "title": book.title,
                    "author": book.author,
                    "borrow_count": count,
                }
            )

        most_active_users = []
        for user_id, count in user_counts.most_common(self.TOP_RESULTS_LIMIT):
            user = user_lookup.get(user_id)
            if user is None:
                continue

            most_active_users.append(
                {
                    "user_id": user.id_user,
                    "full_name": user.full_name,
                    "username": user.username,
                    "borrow_count": count,
                }
            )

        return {
            "most_borrowed_books": most_borrowed_books,
            "most_active_users": most_active_users,
        }

    def get_overdue_borrowings(self) -> list[Borrowing]:
        self._require_librarian()
        borrowings = self.borrowing_repository.get_all()
        results = [
            borrowing
            for borrowing in borrowings
            if (
                borrowing.status == BorrowingStatus.ACTIVE
                and borrowing.end_date < date.today()
            )
        ]

        logger.info("Fetched overdue borrowings: count=%s", len(results))
        return results

    def get_active_borrowings(self) -> list[Borrowing]:
        self._require_librarian()
        borrowings = self.borrowing_repository.get_all()
        results = [
            borrowing
            for borrowing in borrowings
            if borrowing.status == BorrowingStatus.ACTIVE
        ]

        logger.info("Fetched active borrowings: count=%s", len(results))
        return results

    def get_returned_borrowings(self) -> list[Borrowing]:
        self._require_librarian()
        borrowings = self.borrowing_repository.get_all()
        results = [
            borrowing
            for borrowing in borrowings
            if borrowing.status == BorrowingStatus.RETURNED
        ]

        logger.info("Fetched returned borrowings: count=%s", len(results))
        return results

    def _require_librarian(self) -> None:
        user = self.session.require_authentication()

        if user.role != UserRole.LIBRARIAN:
            logger.warning(
                "Permission denied for user id=%s username=%s: librarian access required for report operations",
                user.id_user,
                user.username,
            )
            raise ReportPermissionError(
                "Only librarians can access reports."
            )
