import logging

from Services.borrowing_service import BorrowingService


logger = logging.getLogger(__name__)


class MyBorrowingsScreen:

    def __init__(self, borrowing_service: BorrowingService) -> None:
        self._borrowing_service = borrowing_service

    def display(self, active_only: bool = False) -> None:

        print("\n--- My Borrowings ---")

        if active_only:
            borrowings = (
                self._borrowing_service
                .get_my_active_borrowings()
            )
        else:
            borrowings = (
                self._borrowing_service
                .get_my_borrowing_history()
            )

        if not borrowings:
            logger.info(
                "UI my borrowings empty: active_only=%s",
                active_only,
            )
            print("No borrowings found.")
            return

        for borrowing in borrowings:

            print(f"Borrowing ID : {borrowing.id_borrowing}")
            print(f"Book ID      : {borrowing.book_id}")
            print(f"Start Date   : {borrowing.start_date}")
            print(f"End Date     : {borrowing.end_date}")
            print(f"Status       : {borrowing.status.value}")
            print(f"Returned At  : {borrowing.returned_at}")
            print(f"Fine         : ${borrowing.fine:.2f}")
            print("-" * 35)

        logger.info(
            "UI my borrowings displayed: active_only=%s count=%s",
            active_only,
            len(borrowings),
        )