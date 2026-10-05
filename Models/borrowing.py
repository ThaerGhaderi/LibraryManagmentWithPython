from datetime import date
from enum import Enum


class BorrowingStatus(Enum):
    ACTIVE = "active"
    RETURNED = "returned"


class Borrowing:

    _last_id = 0

    def __init__(
        self,
        book_id: int,
        user_id: int,
        start_date: date,
        end_date: date,
        status: BorrowingStatus = BorrowingStatus.ACTIVE,
        returned_at: date | None = None,
        fine: float = 0.0,
        id_borrowing: int | None = None,
    ) -> None:

        if start_date > end_date:
            raise ValueError(
                "Start date cannot be after end date."
            )

        if book_id <= 0:
            raise ValueError(
                "book_id must be a positive integer."
            )

        if user_id <= 0:
            raise ValueError(
                "user_id must be a positive integer."
            )

        if isinstance(status, str):
            try:
                status = BorrowingStatus(status)
            except ValueError:
                raise ValueError(
                    f"Invalid borrowing status: {status}"
                )

        if not isinstance(status, BorrowingStatus):
            raise TypeError(
                "status must be a BorrowingStatus."
            )

        if fine < 0:
            raise ValueError(
                "Fine cannot be negative."
            )

        if id_borrowing is None:
            Borrowing._last_id += 1
            self._id_borrowing = Borrowing._last_id

        else:
            if id_borrowing <= 0:
                raise ValueError(
                    "id_borrowing must be a positive integer."
                )

            self._id_borrowing = id_borrowing

            if id_borrowing > Borrowing._last_id:
                Borrowing._last_id = id_borrowing

        self._book_id = book_id
        self._user_id = user_id
        self._start_date = start_date
        self._end_date = end_date
        self._status = status
        self._returned_at = returned_at
        self._fine = fine

    @property
    def id_borrowing(self) -> int:
        return self._id_borrowing

    @property
    def book_id(self) -> int:
        return self._book_id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def start_date(self) -> date:
        return self._start_date

    @property
    def end_date(self) -> date:
        return self._end_date

    @property
    def status(self) -> BorrowingStatus:
        return self._status

    @property
    def returned_at(self) -> date | None:
        return self._returned_at

    @property
    def fine(self) -> float:
        return self._fine

    def is_active(self) -> bool:
        return self._status == BorrowingStatus.ACTIVE

    def calculate_duration(self) -> int:
        end = self._returned_at or self._end_date
        return (end - self._start_date).days

    def close(self, returned_at: date, fine: float) -> None:
        if returned_at < self._start_date:
            raise ValueError(
                "Returned date cannot be before start date."
            )

        if fine < 0:
            raise ValueError(
                "Fine cannot be negative."
            )

        self._returned_at = returned_at
        self._fine = fine
        self._status = BorrowingStatus.RETURNED

    def to_dict(self) -> dict:
        return {
            "id_borrowing": self._id_borrowing,
            "book_id": self._book_id,
            "user_id": self._user_id,
            "start_date": self._start_date.isoformat(),
            "end_date": self._end_date.isoformat(),
            "status": self._status.value,
            "returned_at": (
                self._returned_at.isoformat()
                if self._returned_at is not None
                else None
            ),
            "fine": self._fine,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Borrowing":
        returned_at = data.get("returned_at")

        return cls(
            id_borrowing=data["id_borrowing"],
            book_id=data["book_id"],
            user_id=data["user_id"],
            start_date=date.fromisoformat(data["start_date"]),
            end_date=date.fromisoformat(data["end_date"]),
            status=BorrowingStatus(data["status"]),
            returned_at=(
                date.fromisoformat(returned_at)
                if returned_at
                else None
            ),
            fine=float(data.get("fine", 0.0)),
        )

    def __str__(self) -> str:
        return (
            f"Borrowing {self._id_borrowing} | "
            f"Book: {self._book_id} | "
            f"User: {self._user_id} | "
            f"{self._start_date} → {self._end_date} | "
            f"Status: {self._status.value} | "
            f"Fine: ${self._fine:.2f}"
        )