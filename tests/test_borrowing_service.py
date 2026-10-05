from datetime import date, timedelta

import pytest

from Models.book import Book
from Models.borrowing import (
    Borrowing,
    BorrowingStatus,
)

from auth.exceptions import NotAuthenticatedError

from Services.borrowing_service import (
    BookNotAvailableError,
    BookNotFoundError,
    BorrowingLimitExceededError,
)


def test_borrow_book(
    app,
    member_user,
):

    app.session.login(member_user)

    book = Book(
        "Clean Code",
        "Robert Martin",
        2008,
        "Programming",
    )

    app.book_repository.save_all([book])

    borrowing = (
        app.borrowing_service
        .borrow_book(book.id_book)
    )

    assert borrowing.user_id == member_user.id_user
    assert borrowing.book_id == book.id_book
    assert borrowing.status == BorrowingStatus.ACTIVE

    books = app.book_repository.get_all()

    assert books[0].available is False

    borrowings = (
        app.borrowing_repository.get_all()
    )

    assert len(borrowings) == 1


def test_borrow_nonexistent_book(
    app,
    member_user,
):

    app.session.login(member_user)

    with pytest.raises(BookNotFoundError):

        app.borrowing_service.borrow_book(999)


def test_cannot_borrow_unavailable_book(
    app,
    member_user,
):

    app.session.login(member_user)

    book = Book(
        "Unavailable",
        "Author",
        2024,
        "AI",
        available=False,
    )

    app.book_repository.save_all([book])

    with pytest.raises(BookNotAvailableError):

        app.borrowing_service.borrow_book(
            book.id_book
        )


def test_borrowing_limit(
    app,
    member_user,
):

    app.session.login(member_user)

    books = [
        Book(
            f"Book {i}",
            f"Author {i}",
            2020,
            "AI",
        )
        for i in range(1, 7)
    ]

    app.book_repository.save_all(books)

    borrowings = [
        Borrowing(
            book_id=books[i].id_book,
            user_id=member_user.id_user,
            start_date=date.today(),
            end_date=date.today()
            + timedelta(days=14),
        )
        for i in range(5)
    ]

    app.borrowing_repository.save_all(
        borrowings
    )

    with pytest.raises(
        BorrowingLimitExceededError
    ):

        app.borrowing_service.borrow_book(
            books[5].id_book
        )


def test_return_book(
    app,
    member_user,
):

    app.session.login(member_user)

    book = Book(
        "Clean Code",
        "Robert Martin",
        2008,
        "Programming",
    )

    app.book_repository.save_all([book])

    app.borrowing_service.borrow_book(
        book.id_book
    )

    fine = (
        app.borrowing_service
        .return_book(book.id_book)
    )

    assert fine == 0.0

    books = app.book_repository.get_all()

    assert books[0].available is True

    borrowings = (
        app.borrowing_repository.get_all()
    )

    assert (
        borrowings[0].status
        == BorrowingStatus.RETURNED
    )


def test_overdue_fine():

    from Models.borrowing import Borrowing

    borrowing = Borrowing(
        book_id=1,
        user_id=1,
        start_date=date.today()
        - timedelta(days=25),
        end_date=date.today()
        - timedelta(days=5),
    )

    from auth.session import Session
    from Services.borrowing_service import BorrowingService
    from repositories.book_repository import BookRepository
    from repositories.borrowing_repository import BorrowingRepository

    service = BorrowingService(
        session=Session(),
        book_repository=BookRepository(),
        borrowing_repository=BorrowingRepository(),
    )

    fine = service.calculate_fine(
        borrowing=borrowing,
        returned_at=date.today(),
    )

    assert fine > 0


def test_my_active_borrowings(
    app,
    member_user,
):

    app.session.login(member_user)

    book = Book(
        "AI Book",
        "Author",
        2025,
        "AI",
    )

    app.book_repository.save_all([book])

    app.borrowing_service.borrow_book(
        book.id_book
    )

    active = (
        app.borrowing_service
        .get_my_active_borrowings()
    )

    assert len(active) == 1
    assert active[0].book_id == book.id_book


def test_user_cannot_return_another_users_book(
    app,
):

    from Models.user import User, UserRole

    owner = User(
        "Owner",
        "owner",
        "hash",
        "salt",
        UserRole.MEMBER,
    )

    stranger = User(
        "Stranger",
        "stranger",
        "hash",
        "salt",
        UserRole.MEMBER,
    )

    app.user_repository.save_all(
        [owner, stranger]
    )

    book = Book(
        "Private Book",
        "Author",
        2024,
        "AI",
    )

    app.book_repository.save_all([book])

    app.session.login(owner)

    app.borrowing_service.borrow_book(
        book.id_book
    )

    app.session.login(stranger)

    from Services.borrowing_service import (
        BorrowingNotFoundError,
    )

    with pytest.raises(BorrowingNotFoundError):

        app.borrowing_service.return_book(
            book.id_book
        )


def test_borrow_requires_authentication(
    app,
):

    with pytest.raises(NotAuthenticatedError):

        app.borrowing_service.borrow_book(1)