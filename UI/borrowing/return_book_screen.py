import logging

from Services.borrowing_service import (
    BorrowingService,
    BookNotFoundError,
    BorrowingNotFoundError,
)


logger = logging.getLogger(__name__)


class ReturnBookScreen:

    def __init__(self, borrowing_service: BorrowingService) -> None:
        self._borrowing_service = borrowing_service

    def display(self) -> None:
        print("\n--- Return Book ---")

        book_id = input(
            "Enter the ID of the book you want to return: "
        ).strip()

        try:
            fine = self._borrowing_service.return_book(
                int(book_id)
            )

            print(
                f"✅ Successfully returned book "
                f"with ID {book_id}."
            )

            if fine > 0:
                print(
                    f"⚠️ Fine: ${fine:.2f}"
                )
            else:
                print("✅ No fine.")

            logger.info(
                "UI return success: book_id=%s fine=%.2f",
                book_id,
                fine,
            )

        except ValueError:
            logger.warning("UI return validation error: invalid book id")
            print("❌ Invalid book ID.")

        except BookNotFoundError as exc:
            logger.warning("UI return failed: %s", exc)
            print(f"❌ {exc}")

        except BorrowingNotFoundError as exc:
            logger.warning("UI return failed: %s", exc)
            print(f"❌ {exc}")