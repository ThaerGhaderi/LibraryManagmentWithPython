import logging

from Services.book_service import (
    BookService,
    BookNotFoundError,
    BookAlreadyExistsError,
    BookPermissionError,
)


logger = logging.getLogger(__name__)


class UpdateBookScreen:

    def __init__(
        self,
        book_service: BookService,
    ) -> None:

        self.book_service = book_service

    def display(self) -> None:

        print("\n--- Update Book ---")

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

            print("\nCurrent data:")
            print(book)

            print(
                "\nPress Enter to keep the current value."
            )

            title = input(
                f"Title [{book.title}]: "
            ).strip()

            author = input(
                f"Author [{book.author}]: "
            ).strip()

            year_input = input(
                f"Year [{book.year}]: "
            ).strip()

            classification = input(
                f"Classification "
                f"[{', '.join(book.classification)}]: "
            ).strip()

            site = input(
                f"Publication site "
                f"[{book.publication_site or 'none'}]: "
            ).strip()

            year = (
                int(year_input)
                if year_input
                else None
            )

            updated_book = self.book_service.update_book(
                book_id=book_id,
                title=title or None,
                author=author or None,
                year=year,
                classification=(
                    classification or None
                ),
                publication_site=(
                    site or None
                ),
            )

            print("\n✅ Book updated successfully.")
            print(updated_book)
            logger.info(
                "UI book update success: id=%s title=%s author=%s",
                updated_book.id_book,
                updated_book.title,
                updated_book.author,
            )

        except ValueError as exc:
            logger.warning("UI book update validation error: %s", exc)
            print(f"❌ {exc}")

        except (
            BookNotFoundError,
            BookAlreadyExistsError,
            BookPermissionError,
        ) as exc:
            logger.warning("UI book update failed: %s", exc)
            print(f"❌ {exc}")