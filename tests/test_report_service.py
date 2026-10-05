from datetime import date, timedelta

import pytest

from Models.book import Book
from Models.user import User, UserRole
from Models.borrowing import (
    Borrowing,
    BorrowingStatus,
)

from Services.report_service import (
    ReportPermissionError,
)


def test_generate_report(
    app,
    librarian_user,
):

    app.session.login(librarian_user)

    member1 = User(
        "Member One",
        "member1",
        "hash",
        "salt",
        UserRole.MEMBER,
    )

    member2 = User(
        "Member Two",
        "member2",
        "hash",
        "salt",
        UserRole.MEMBER,
    )

    app.user_repository.save_all(
        [
            librarian_user,
            member1,
            member2,
        ]
    )

    book1 = Book(
        "Python",
        "Author 1",
        2024,
        "Python",
    )

    book2 = Book(
        "AI",
        "Author 2",
        2025,
        "AI",
        available=False,
    )

    book3 = Book(
        "Algorithms",
        "Author 3",
        2020,
        "Algorithms",
    )

    app.book_repository.save_all(
        [book1, book2, book3]
    )

    borrowing1 = Borrowing(
        book_id=book1.id_book,
        user_id=member1.id_user,
        start_date=date.today()
        - timedelta(days=30),
        end_date=date.today()
        - timedelta(days=16),
        status=BorrowingStatus.RETURNED,
        returned_at=date.today()
        - timedelta(days=15),
        fine=2.0,
    )

    borrowing2 = Borrowing(
        book_id=book1.id_book,
        user_id=member1.id_user,
        start_date=date.today()
        - timedelta(days=20),
        end_date=date.today()
        - timedelta(days=6),
        status=BorrowingStatus.RETURNED,
        returned_at=date.today()
        - timedelta(days=5),
        fine=1.0,
    )

    borrowing3 = Borrowing(
        book_id=book2.id_book,
        user_id=member2.id_user,
        start_date=date.today()
        - timedelta(days=25),
        end_date=date.today()
        - timedelta(days=5),
        status=BorrowingStatus.ACTIVE,
    )

    app.borrowing_repository.save_all(
        [
            borrowing1,
            borrowing2,
            borrowing3,
        ]
    )

    report = (
        app.report_service
        .generate_report()
    )

    assert report["books"]["total"] == 3
    assert report["books"]["available"] == 2
    assert report["books"]["borrowed"] == 1

    assert report["users"]["total"] == 3
    assert report["users"]["members"] == 2
    assert report["users"]["librarians"] == 1

    assert report["borrowings"]["total"] == 3
    assert report["borrowings"]["active"] == 1
    assert report["borrowings"]["returned"] == 2
    assert report["borrowings"]["overdue"] == 1

    assert report["borrowings"]["total_fines"] == 3.0

    most_borrowed = (
        report["rankings"]
        ["most_borrowed_books"]
    )

    assert most_borrowed[0]["book_id"] == book1.id_book
    assert most_borrowed[0]["borrow_count"] == 2

    most_active = (
        report["rankings"]
        ["most_active_users"]
    )

    assert most_active[0]["user_id"] == member1.id_user
    assert most_active[0]["borrow_count"] == 2


def test_overdue_report(
    app,
    librarian_user,
):

    app.session.login(librarian_user)

    member = User(
        "Member",
        "member",
        "hash",
        "salt",
        UserRole.MEMBER,
    )

    app.user_repository.save_all(
        [
            librarian_user,
            member,
        ]
    )

    overdue = Borrowing(
        book_id=1,
        user_id=member.id_user,
        start_date=date.today()
        - timedelta(days=30),
        end_date=date.today()
        - timedelta(days=5),
        status=BorrowingStatus.ACTIVE,
    )

    app.borrowing_repository.save_all(
        [overdue]
    )

    results = (
        app.report_service
        .get_overdue_borrowings()
    )

    assert len(results) == 1
    assert results[0].id_borrowing == overdue.id_borrowing


def test_member_cannot_access_reports(
    app,
    member_user,
):

    app.session.login(member_user)

    with pytest.raises(
        ReportPermissionError
    ):

        app.report_service.generate_report()