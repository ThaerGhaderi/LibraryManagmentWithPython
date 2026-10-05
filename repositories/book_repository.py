import logging

from Models.book import Book
from Storage.json_storage import JSONStorage


logger = logging.getLogger(__name__)


class BookRepository:

    def __init__(self) -> None:
        self.storage = JSONStorage[Book](
            "books.json"
        )

    def get_all(self) -> list[Book]:
        books = self.storage.load_all(
            Book.from_dict
        )
        logger.debug("Books loaded from repository: count=%s", len(books))
        return books

    def save_all(
        self,
        books: list[Book],
    ) -> None:
        self.storage.save_all(
            books,
            Book.to_dict,
        )
        logger.info("Books saved to repository: count=%s", len(books))