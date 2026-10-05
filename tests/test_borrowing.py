from datetime import date, timedelta

import pytest

from Models.borrowing import (
    Borrowing,
    BorrowingStatus,
)


def test_borrowing_creation():

    borrowing = Borrowing(
        book_id=1,
        user_id=2,
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 15),
    )

    assert borrowing.book_id == 1
    assert borrowing.user_id == 2
    assert borrowing.status == BorrowingStatus.ACTIVE
    assert borrowing.returned_at is None
    assert borrowing.fine == 0.0


def test_invalid_borrowing_dates():

    with pytest.raises(ValueError):
        Borrowing(
            book_id=1,
            user_id=1,
            start_date=date(2026, 10, 20),
            end_date=date(2026, 10, 10),
        )


def test_borrowing_duration():

    borrowing = Borrowing(
        1,
        1,
        date(2026, 10, 1),
        date(2026, 10, 10),
    )

    assert borrowing.calculate_duration() == 9


def test_borrowing_close():

    borrowing = Borrowing(
        1,
        1,
        date(2026, 10, 1),
        date(2026, 10, 15),
    )

    returned_at = date(2026, 10, 18)

    borrowing.close(
        returned_at=returned_at,
        fine=3.0,
    )

    assert borrowing.status == BorrowingStatus.RETURNED
    assert borrowing.returned_at == returned_at
    assert borrowing.fine == 3.0


def test_borrowing_serialization_round_trip():

    borrowing = Borrowing(
        book_id=5,
        user_id=3,
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 15),
        status=BorrowingStatus.RETURNED,
        returned_at=date(2026, 10, 17),
        fine=2.0,
    )

    data = borrowing.to_dict()

    restored = Borrowing.from_dict(data)

    assert restored.id_borrowing == borrowing.id_borrowing
    assert restored.book_id == borrowing.book_id
    assert restored.user_id == borrowing.user_id
    assert restored.start_date == borrowing.start_date
    assert restored.end_date == borrowing.end_date
    assert restored.status == borrowing.status
    assert restored.returned_at == borrowing.returned_at
    assert restored.fine == borrowing.fine