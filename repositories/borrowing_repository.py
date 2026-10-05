import logging

from Models.borrowing import Borrowing
from Storage.json_storage import JSONStorage


logger = logging.getLogger(__name__)


class BorrowingRepository:

    def __init__(self) -> None:
        self.storage = JSONStorage[Borrowing](
            "borrowings.json"
        )

    def get_all(self) -> list[Borrowing]:
        borrowings = self.storage.load_all(
            Borrowing.from_dict
        )
        logger.debug(
            "Borrowings loaded from repository: count=%s",
            len(borrowings),
        )
        return borrowings

    def save_all(
        self,
        borrowings: list[Borrowing],
    ) -> None:
        self.storage.save_all(
            borrowings,
            Borrowing.to_dict,
        )
        logger.info(
            "Borrowings saved to repository: count=%s",
            len(borrowings),
        )