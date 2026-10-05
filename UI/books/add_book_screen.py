import logging

from Services.book_service import (
    BookService,
    BookAlreadyExistsError,
)
from Models.book import Book


logger = logging.getLogger(__name__)


class AddBookScreen:

    def __init__(
        self,
        book_service: BookService,
    ) -> None:

        self.book_service = book_service

    def display(self) -> None:

        print("\n--- Add Book ---")

        try:
            title = input("Title: ")
            author = input("Author: ")
            year = int(input("Year: "))

            classification = input(
                "Classification (comma separated): "
            )

            publication_site = input(
                "Publication site: "
            )

            book = Book(
                title=title,
                author=author,
                year=year,
                classification=classification,
                publication_site=publication_site,
            )

            book = self.book_service.add_book(book)

            print(
                f"✅ Book added successfully."
                f"\nBook ID: {book.id_book}"
            )
            logger.info(
                "UI book add success: id=%s title=%s author=%s",
                book.id_book,
                book.title,
                book.author,
            )

        except ValueError as exc:
            logger.warning("UI book add validation error: %s", exc)
            print(f"❌ {exc}")

        except BookAlreadyExistsError as exc:
            logger.warning("UI book add failed: %s", exc)
            print(f"❌ {exc}")