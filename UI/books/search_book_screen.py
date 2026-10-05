import logging

from Services.book_service import BookService


logger = logging.getLogger(__name__)


class SearchBookScreen:

    def __init__(
        self,
        book_service: BookService,
    ) -> None:

        self.book_service = book_service

    def display(self) -> None:

        print("\n--- Search Books ---")
        print("1. By ID")
        print("2. By Title")
        print("3. By Author")
        print("4. By Classification")

        choice = input("Choose: ").strip()

        if choice == "1":
            self._search_by_id()

        elif choice == "2":
            self._search_by_title()

        elif choice == "3":
            self._search_by_author()

        elif choice == "4":
            self._search_by_classification()

        else:
            logger.warning("UI book search invalid choice: %s", choice)
            print("❌ Invalid choice.")

    def _search_by_id(self) -> None:

        try:
            book_id = int(input("Book ID: "))

            book = self.book_service.find_book_by_id(
                book_id
            )

            if book is None:
                logger.info("UI book search by id found no result: id=%s", book_id)
                print("❌ Book not found.")
                return

            print(book)
            logger.info("UI book search by id success: id=%s", book_id)

        except ValueError:
            logger.warning("UI book search by id validation error")
            print("❌ Invalid ID.")

    def _search_by_title(self) -> None:

        title = input("Title: ")

        books = self.book_service.search_by_title(
            title
        )

        self._display_results(books)

    def _search_by_author(self) -> None:

        author = input("Author: ")

        books = self.book_service.search_by_author(
            author
        )

        self._display_results(books)

    def _search_by_classification(self) -> None:

        classification = input(
            "Classification: "
        )

        books = (
            self.book_service
            .search_by_classification(classification)
        )

        self._display_results(books)

    @staticmethod
    def _display_results(books) -> None:

        if not books:
            logger.info("UI book search returned no results")
            print("No books found.")
            return

        print()

        for book in books:
            print(book)

        print(f"\nFound: {len(books)}")
        logger.info("UI book search returned results: count=%s", len(books))