import logging
from datetime import date, timedelta

import config.config as config
from Models.book import Book
from Models.borrowing import Borrowing, BorrowingStatus
from auth.session import Session
from repositories.book_repository import BookRepository
from repositories.borrowing_repository import BorrowingRepository


logger = logging.getLogger(__name__)


class BorrowingError(Exception):
    """Base exception for borrowing operations."""


class BookNotFoundError(BorrowingError):
    pass


class BookNotAvailableError(BorrowingError):
    pass


class AlreadyBorrowedError(BorrowingError):
    pass


class BorrowingLimitExceededError(BorrowingError):
    pass


class BorrowingNotFoundError(BorrowingError):
    pass


class BorrowingService:

    def __init__(
        self,
        session: Session,
        book_repository: BookRepository,
        borrowing_repository: BorrowingRepository,
    ) -> None:
        self.session = session
        self.book_repository = book_repository
        self.borrowing_repository = borrowing_repository

    def borrow_book(self, book_id: int) -> Borrowing:
        user = self.session.require_authentication()
        books = self.book_repository.get_all()
        book = self._find_book(
            books,
            book_id,
        )

        if book is None:
            logger.warning(
                "Borrowing failed for user id=%s username=%s: book not found id=%s",
                user.id_user,
                user.username,
                book_id,
            )
            raise BookNotFoundError(
                f"Book with ID {book_id} was not found."
            )

        if not book._available:
            logger.warning(
                "Borrowing failed for user id=%s username=%s: book not available id=%s",
                user.id_user,
                user.username,
                book_id,
            )
            raise BookNotAvailableError(
                f"Book with ID {book_id} is not available."
            )

        borrowings = self.borrowing_repository.get_all()
        active_user_borrowings = [
            borrowing
            for borrowing in borrowings
            if (
                borrowing.user_id == user.id_user
                and borrowing.status == BorrowingStatus.ACTIVE
            )
        ]

        if len(active_user_borrowings) >= config.MAX_ACTIVE_BORROWINGS:
            logger.warning(
                "Borrowing failed for user id=%s username=%s: active borrowing limit reached",
                user.id_user,
                user.username,
            )
            raise BorrowingLimitExceededError(
                f"You cannot borrow more than "
                f"{config.MAX_ACTIVE_BORROWINGS} books."
            )

        already_borrowed = any(
            borrowing.book_id == book_id
            and borrowing.user_id == user.id_user
            and borrowing.status == BorrowingStatus.ACTIVE
            for borrowing in borrowings
        )

        if already_borrowed:
            logger.warning(
                "Borrowing failed for user id=%s username=%s: book already borrowed id=%s",
                user.id_user,
                user.username,
                book_id,
            )
            raise AlreadyBorrowedError(
                "You already borrowed this book."
            )

        start_date = date.today()
        end_date = start_date + timedelta(
            days=config.BORROWING_PERIOD_DAYS
        )
        borrowing = Borrowing(
            book_id=book.id_book,
            user_id=user.id_user,
            start_date=start_date,
            end_date=end_date,
        )

        borrowings.append(borrowing)
        book.update_available(False)
        self.book_repository.save_all(books)
        self.borrowing_repository.save_all(borrowings)

        logger.info(
            "Book borrowed: borrowing_id=%s user_id=%s username=%s book_id=%s",
            borrowing.id_borrowing,
            user.id_user,
            user.username,
            book.id_book,
        )

        return borrowing

    def return_book(self, book_id: int) -> float:
        user = self.session.require_authentication()
        books = self.book_repository.get_all()
        book = self._find_book(
            books,
            book_id,
        )

        if book is None:
            logger.warning(
                "Return failed for user id=%s username=%s: book not found id=%s",
                user.id_user,
                user.username,
                book_id,
            )
            raise BookNotFoundError(
                f"Book with ID {book_id} was not found."
            )

        borrowings = self.borrowing_repository.get_all()
        borrowing = self._find_active_borrowing(
            borrowings=borrowings,
            user_id=user.id_user,
            book_id=book_id,
        )

        if borrowing is None:
            logger.warning(
                "Return failed for user id=%s username=%s: active borrowing not found for book_id=%s",
                user.id_user,
                user.username,
                book_id,
            )
            raise BorrowingNotFoundError(
                "No active borrowing was found "
                "for this book and user."
            )

        today = date.today()
        fine = self.calculate_fine(
            borrowing=borrowing,
            returned_at=today,
        )

        borrowing.close(
            returned_at=today,
            fine=fine,
        )
        book.update_available(True)
        self.book_repository.save_all(books)
        self.borrowing_repository.save_all(borrowings)

        logger.info(
            "Book returned: borrowing_id=%s user_id=%s username=%s book_id=%s fine=%.2f",
            borrowing.id_borrowing,
            user.id_user,
            user.username,
            book.id_book,
            fine,
        )

        return fine

    def get_my_borrowings(self) -> list[Borrowing]:
        user = self.session.require_authentication()
        borrowings = self.borrowing_repository.get_all()
        results = [
            borrowing
            for borrowing in borrowings
            if borrowing.user_id == user.id_user
        ]

        logger.info(
            "Fetched my borrowings: user_id=%s username=%s count=%s",
            user.id_user,
            user.username,
            len(results),
        )
        return results

    def get_my_active_borrowings(
        self,
    ) -> list[Borrowing]:
        user = self.session.require_authentication()
        borrowings = self.borrowing_repository.get_all()
        results = [
            borrowing
            for borrowing in borrowings
            if (
                borrowing.user_id == user.id_user
                and borrowing.status == BorrowingStatus.ACTIVE
            )
        ]

        logger.info(
            "Fetched my active borrowings: user_id=%s username=%s count=%s",
            user.id_user,
            user.username,
            len(results),
        )
        return results

    def get_my_borrowing_history(
        self,
    ) -> list[Borrowing]:
        user = self.session.require_authentication()
        borrowings = self.borrowing_repository.get_all()
        results = [
            borrowing
            for borrowing in borrowings
            if borrowing.user_id == user.id_user
        ]

        logger.info(
            "Fetched my borrowing history: user_id=%s username=%s count=%s",
            user.id_user,
            user.username,
            len(results),
        )
        return results

    def calculate_fine(
    self,
    borrowing: Borrowing,
    returned_at: date,
     ) -> float:

     if returned_at <= borrowing.end_date:
        return 0.0

     overdue_days = (
        returned_at - borrowing.end_date
     ).days

     first_period_days = min(
        overdue_days,
        config.FINE_FIRST_PERIOD_DAYS,
     )

     remaining_days = max(
        overdue_days
        - config.FINE_FIRST_PERIOD_DAYS,
        0,
     )

     fine = (
        first_period_days
        * config.FINE_FIRST_PERIOD_RATE
     )

     fine += (
        remaining_days
        * config.FINE_AFTER_FIRST_PERIOD_RATE
    )

     return fine

    @staticmethod
    def _find_book(
        books: list[Book],
        book_id: int,
    ) -> Book | None:
        for book in books:
            if book.id_book == book_id:
                return book

        return None

    @staticmethod
    def _find_active_borrowing(
        borrowings: list[Borrowing],
        user_id: int,
        book_id: int,
    ) -> Borrowing | None:
        for borrowing in borrowings:
            if (
                borrowing.user_id == user_id
                and borrowing.book_id == book_id
                and borrowing.status == BorrowingStatus.ACTIVE
            ):
                return borrowing

        return None
