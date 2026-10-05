import logging

from Services.book_service import BookService
from Models.user import UserRole

from UI.books.add_book_screen import AddBookScreen
from UI.books.search_book_screen import SearchBookScreen
from UI.books.list_books_screen import ListBooksScreen
from UI.books.update_book_screen import UpdateBookScreen
from UI.books.delete_book_screen import DeleteBookScreen


logger = logging.getLogger(__name__)


class BooksMenu:

    def __init__(
        self,
        book_service: BookService,
    ) -> None:

        self.book_service = book_service

        self.add_screen = AddBookScreen(
            book_service
        )

        self.search_screen = SearchBookScreen(
            book_service
        )

        self.list_screen = ListBooksScreen(
            book_service
        )

        self.update_screen = UpdateBookScreen(
            book_service
        )

        self.delete_screen = DeleteBookScreen(
            book_service
        )

    def display_menu(self) -> None:

        user = self.book_service.session.require_authentication()

        print("\n" + "=" * 35)
        print("          BOOKS MENU")
        print("=" * 35)

        if user.role == UserRole.LIBRARIAN:

            print("1. Add Book")
            print("2. List All Books")
            print("3. Search Books")
            print("4. Update Book")
            print("5. Delete Book")
            print("6. Available Books")
            print("7. Borrowed Books")

        else:

            print("1. List All Books")
            print("2. Search Books")
            print("3. Available Books")
            print("4. Borrowed Books")

        print("0. Back")

    def run(self) -> None:

        while self.book_service.session.is_authenticated:

            self.display_menu()

            choice = input(
                "Enter your choice: "
            ).strip()

            user = (
                self.book_service
                .session
                .require_authentication()
            )

            if user.role == UserRole.LIBRARIAN:

                if choice == "1":
                    self.add_screen.display()

                elif choice == "2":
                    self.list_screen.display("all")

                elif choice == "3":
                    self.search_screen.display()

                elif choice == "4":
                    self.update_screen.display()

                elif choice == "5":
                    self.delete_screen.display()

                elif choice == "6":
                    self.list_screen.display("available")

                elif choice == "7":
                    self.list_screen.display("borrowed")

                elif choice == "0":
                    logger.info("Books menu exited by librarian")
                    return

                else:
                    logger.warning("Invalid books menu choice for librarian: %s", choice)
                    print("❌ Invalid choice.")

            else:

                if choice == "1":
                    self.list_screen.display("all")

                elif choice == "2":
                    self.search_screen.display()

                elif choice == "3":
                    self.list_screen.display("available")

                elif choice == "4":
                    self.list_screen.display("borrowed")

                elif choice == "0":
                    logger.info("Books menu exited by member")
                    return

                else:
                    logger.warning("Invalid books menu choice for member: %s", choice)
                    print("❌ Invalid choice.")