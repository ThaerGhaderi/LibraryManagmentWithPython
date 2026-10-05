import logging

from Services.borrowing_service import (
    BorrowingService,
    BookNotFoundError,
    BookNotAvailableError,
    AlreadyBorrowedError,
    BorrowingLimitExceededError,
)


logger = logging.getLogger(__name__)


class BorrowBookScreen:

    def __init__(self, borrowing_service: BorrowingService) -> None:
        self._borrowing_service = borrowing_service

    def display(self) -> None:
        print("\n--- Borrow Book ---")

        book_id = input(
            "Enter the ID of the book you want to borrow: "
        ).strip()

        try:
            borrowing = self._borrowing_service.borrow_book(
                int(book_id)
            )

            print(
                f"✅ Successfully borrowed book "
                f"with ID {book_id}."
            )

            print(
                f"Return date: {borrowing.end_date}"
            )
            logger.info(
                "UI borrow success: book_id=%s borrowing_id=%s",
                book_id,
                borrowing.id_borrowing,
            )

        except ValueError:
            logger.warning("UI borrow validation error: invalid book id")
            print("❌ Invalid book ID.")

        except BookNotFoundError as exc:
            logger.warning("UI borrow failed: %s", exc)
            print(f"❌ {exc}")

        except BookNotAvailableError as exc:
            logger.warning("UI borrow failed: %s", exc)
            print(f"❌ {exc}")

        except AlreadyBorrowedError as exc:
            logger.warning("UI borrow failed: %s", exc)
            print(f"❌ {exc}")

        except BorrowingLimitExceededError as exc:
            logger.warning("UI borrow failed: %s", exc)
            print(f"❌ {exc}")