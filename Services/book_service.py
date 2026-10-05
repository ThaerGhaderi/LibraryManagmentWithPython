import logging

from Models.book import Book
from Models.user import UserRole
from auth.session import Session
from repositories.book_repository import BookRepository


logger = logging.getLogger(__name__)


class BookError(Exception):
    """Base exception for book operations."""


class BookAlreadyExistsError(BookError):
    pass


class BookNotFoundError(BookError):
    pass


class BookPermissionError(BookError):
    pass


class BookService:
    def __init__(
        self,
        repository: BookRepository,
        session: Session,
    ) -> None:
        self.repository = repository
        self.session = session

    def add_book(self, book: Book) -> Book:
        self._require_librarian()

        books = self.repository.get_all()

        if self._is_duplicate(book, books):
            logger.warning(
                "Book creation failed: duplicate title=%s author=%s",
                book.title,
                book.author,
            )
            raise BookAlreadyExistsError(
                f"Book '{book.title}' by "
                f"'{book.author}' already exists."
            )

        books.append(book)
        self.repository.save_all(books)

        logger.info(
            "Book added: id=%s title=%s author=%s available=%s",
            book.id_book,
            book.title,
            book.author,
            book.available,
        )

        return book

    def get_all_books(self) -> list[Book]:
        books = self.repository.get_all()
        logger.info("Fetched all books: count=%s", len(books))
        return books

    def find_book_by_id(
        self,
        book_id: int,
    ) -> Book | None:
        books = self.repository.get_all()

        for book in books:
            if book.id_book == book_id:
                logger.info(
                    "Book found by id: id=%s title=%s",
                    book.id_book,
                    book.title,
                )
                return book

        logger.warning("Book not found by id=%s", book_id)
        return None

    def search_by_title(
        self,
        title: str,
    ) -> list[Book]:
        query = title.strip().lower()

        if not query:
            logger.warning("Book title search skipped: empty query")
            return []

        books = self.repository.get_all()
        results = [
            book
            for book in books
            if query in book.title.lower()
        ]

        logger.info(
            "Books searched by title: query=%s results=%s",
            query,
            len(results),
        )
        return results

    def search_by_author(
        self,
        author: str,
    ) -> list[Book]:
        query = author.strip().lower()

        if not query:
            logger.warning("Book author search skipped: empty query")
            return []

        books = self.repository.get_all()
        results = [
            book
            for book in books
            if query in book.author.lower()
        ]

        logger.info(
            "Books searched by author: query=%s results=%s",
            query,
            len(results),
        )
        return results

    def search_by_classification(
        self,
        classification: str,
    ) -> list[Book]:
        query = classification.strip().lower()

        if not query:
            logger.warning(
                "Book classification search skipped: empty query"
            )
            return []

        books = self.repository.get_all()
        results = [
            book
            for book in books
            if any(
                query in item.lower()
                for item in book.classification
            )
        ]

        logger.info(
            "Books searched by classification: query=%s results=%s",
            query,
            len(results),
        )
        return results

    def get_available_books(self) -> list[Book]:
        books = [
            book
            for book in self.repository.get_all()
            if book.available
        ]
        logger.info("Fetched available books: count=%s", len(books))
        return books

    def get_borrowed_books(self) -> list[Book]:
        books = [
            book
            for book in self.repository.get_all()
            if not book.available
        ]
        logger.info("Fetched borrowed books: count=%s", len(books))
        return books

    def update_book(
        self,
        book_id: int,
        title: str | None = None,
        author: str | None = None,
        year: int | None = None,
        classification=None,
        publication_site: str | None = None,
    ) -> Book:
        self._require_librarian()

        books = self.repository.get_all()
        book = self._find_in_list(
            books,
            book_id,
        )

        if book is None:
            logger.warning("Book update failed: book not found id=%s", book_id)
            raise BookNotFoundError(
                f"Book with ID {book_id} was not found."
            )

        new_title = (
            title.strip().lower()
            if title is not None
            else book.title.lower()
        )
        new_author = (
            author.strip().lower()
            if author is not None
            else book.author.lower()
        )

        for other_book in books:
            if other_book.id_book == book_id:
                continue

            if (
                other_book.title.strip().lower() == new_title
                and other_book.author.strip().lower() == new_author
            ):
                logger.warning(
                    "Book update failed for id=%s: duplicate title=%s author=%s",
                    book_id,
                    new_title,
                    new_author,
                )
                raise BookAlreadyExistsError(
                    "Another book with the same "
                    "title and author already exists."
                )

        book.update_details(
            title=title,
            author=author,
            year=year,
            classification=classification,
            publication_site=publication_site,
        )
        self.repository.save_all(books)

        logger.info(
            "Book updated: id=%s title=%s author=%s",
            book.id_book,
            book.title,
            book.author,
        )

        return book

    def delete_book(
        self,
        book_id: int,
    ) -> Book:
        self._require_librarian()

        books = self.repository.get_all()

        for index, book in enumerate(books):
            if book.id_book == book_id:
                if not book.available:
                    logger.warning(
                        "Book delete failed: borrowed book id=%s",
                        book_id,
                    )
                    raise BookError(
                        "Borrowed books cannot be deleted."
                    )

                deleted_book = books.pop(index)
                self.repository.save_all(books)

                logger.info(
                    "Book deleted: id=%s title=%s author=%s",
                    deleted_book.id_book,
                    deleted_book.title,
                    deleted_book.author,
                )

                return deleted_book

        logger.warning("Book delete failed: book not found id=%s", book_id)
        raise BookNotFoundError(
            f"Book with ID {book_id} was not found."
        )

    @staticmethod
    def _find_in_list(
        books: list[Book],
        book_id: int,
    ) -> Book | None:
        for book in books:
            if book.id_book == book_id:
                return book

        return None

    @staticmethod
    def _is_duplicate(
        new_book: Book,
        books: list[Book],
    ) -> bool:
        title = new_book.title.strip().lower()
        author = new_book.author.strip().lower()

        return any(
            book.title.strip().lower() == title
            and book.author.strip().lower() == author
            for book in books
        )

    def _require_librarian(self) -> None:
        user = self.session.require_authentication()

        if user.role != UserRole.LIBRARIAN:
            logger.warning(
                "Permission denied for user id=%s username=%s: librarian access required for book operations",
                user.id_user,
                user.username,
            )
            raise BookPermissionError(
                "Only librarians can perform this operation."
            )
