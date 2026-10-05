import logging

from Services.book_service import (
    BookService,
    BookNotFoundError,
    BookPermissionError,
    BookError,
)


logger = logging.getLogger(__name__)


class DeleteBookScreen:

    def __init__(
        self,
        book_service: BookService,
    ) -> None:

        self.book_service = book_service

    def display(self) -> None:

        print("\n--- Delete Book ---")

        try:
            book_id = int(
                input("Book ID: ")
            )

            book = self.book_service.find_book_by_id(
                book_id
            )

            if book is None:
                print("❌ Book not found.")
                return

            print(book)

            confirmation = input(
                "Are you sure? (y/n): "
            ).strip().lower()

            if confirmation != "y":
                print("Operation cancelled.")
                return

            self.book_service.delete_book(
                book_id
            )

            print("✅ Book deleted successfully.")
            logger.info("UI book delete success: id=%s", book_id)

        except ValueError:
            logger.warning("UI book delete validation error: invalid id input")
            print("❌ Invalid ID.")

        except (
            BookNotFoundError,
            BookPermissionError,
            BookError,
        ) as exc:
            logger.warning("UI book delete failed: %s", exc)
            print(f"❌ {exc}")