import logging

from Services.book_service import BookService


logger = logging.getLogger(__name__)


class ListBooksScreen:

    def __init__(
        self,
        book_service: BookService,
    ) -> None:

        self.book_service = book_service

    def display(
        self,
        mode: str = "all",
    ) -> None:

        if mode == "available":
            books = self.book_service.get_available_books()

        elif mode == "borrowed":
            books = self.book_service.get_borrowed_books()

        else:
            books = self.book_service.get_all_books()

        print("\n--- Books ---")

        if not books:
            logger.info("UI book list returned no results for mode=%s", mode)
            print("No books found.")
            return

        for book in books:
            print(book)

        print(f"\nTotal: {len(books)}")
        logger.info("UI book list displayed: mode=%s count=%s", mode, len(books))