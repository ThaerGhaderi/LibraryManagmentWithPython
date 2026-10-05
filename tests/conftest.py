from types import SimpleNamespace

import pytest

from Storage.json_storage import JSONStorage

from Models.book import Book
from Models.user import User, UserRole
from Models.borrowing import Borrowing

from repositories.book_repository import BookRepository
from repositories.user_repository import UserRepository
from repositories.borrowing_repository import BorrowingRepository

from Services.auth_service import AuthService
from Services.user_service import UserService
from Services.book_service import BookService
from Services.borrowing_service import BorrowingService
from Services.report_service import ReportService

from auth.session import Session


@pytest.fixture(autouse=True)
def reset_model_counters():
    """
    Keep tests isolated from class-level ID counters.
    """

    if hasattr(Book, "_last_id"):
        Book._last_id = 0
    elif hasattr(Book, "id_book"):
        Book.id_book = 0

    if hasattr(User, "_last_id"):
        User._last_id = 0
    elif hasattr(User, "user_id"):
        User.user_id = 0

    if hasattr(Borrowing, "_last_id"):
        Borrowing._last_id = 0


@pytest.fixture
def app(tmp_path):
    """
    Creates a completely isolated application environment.

    No test touches the real data/ directory.
    """

    session = Session()

    book_repository = BookRepository()
    user_repository = UserRepository()
    borrowing_repository = BorrowingRepository()

    # Replace real storage with temporary test storage.
    book_repository.storage = JSONStorage[Book](
        "books.json",
        data_dir=tmp_path,
    )

    user_repository.storage = JSONStorage[User](
        "users.json",
        data_dir=tmp_path,
    )

    borrowing_repository.storage = JSONStorage[Borrowing](
        "borrowings.json",
        data_dir=tmp_path,
    )

    auth_service = AuthService(
        user_repository=user_repository,
        session=session,
    )

    user_service = UserService(
        user_repository=user_repository,
        session=session,
    )

    book_service = BookService(
        repository=book_repository,
        session=session,
    )

    borrowing_service = BorrowingService(
        session=session,
        book_repository=book_repository,
        borrowing_repository=borrowing_repository,
    )

    report_service = ReportService(
        session=session,
        book_repository=book_repository,
        user_repository=user_repository,
        borrowing_repository=borrowing_repository,
    )

    return SimpleNamespace(
        session=session,
        book_repository=book_repository,
        user_repository=user_repository,
        borrowing_repository=borrowing_repository,
        auth_service=auth_service,
        user_service=user_service,
        book_service=book_service,
        borrowing_service=borrowing_service,
        report_service=report_service,
    )


@pytest.fixture
def member_user(app):
    user = User(
        full_name="Test Member",
        username="member",
        password_hash="test_hash",
        salt="test_salt",
        role=UserRole.MEMBER,
    )

    app.user_repository.save_all([user])

    return user


@pytest.fixture
def librarian_user(app):
    user = User(
        full_name="Test Librarian",
        username="librarian",
        password_hash="test_hash",
        salt="test_salt",
        role=UserRole.LIBRARIAN,
    )

    app.user_repository.save_all([user])

    return user