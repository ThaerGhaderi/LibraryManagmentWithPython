import logging

from Services.borrowing_service import BorrowingService

from UI.borrowing.borrow_book_screen import (
    BorrowBookScreen,
)

from UI.borrowing.return_book_screen import (
    ReturnBookScreen,
)

from UI.borrowing.my_borrowings_screen import (
    MyBorrowingsScreen,
)


logger = logging.getLogger(__name__)


class BorrowingMenu:

    def __init__(
        self,
        borrowing_service: BorrowingService,
    ) -> None:

        self._borrowing_service = borrowing_service

        self._borrow_book_screen = (
            BorrowBookScreen(borrowing_service)
        )

        self._return_book_screen = (
            ReturnBookScreen(borrowing_service)
        )

        self._my_borrowings_screen = (
            MyBorrowingsScreen(borrowing_service)
        )

    def display_menu(self) -> None:

        print("\n" + "=" * 35)
        print("         BORROWING MENU")
        print("=" * 35)

        print("1. Borrow Book")
        print("2. Return Book")
        print("3. My Active Borrowings")
        print("4. My Borrowing History")
        print("0. Back")

    def run(self) -> None:

        while True:

            self.display_menu()

            choice = input(
                "Enter your choice: "
            ).strip()

            if choice == "1":
                self._borrow_book_screen.display()

            elif choice == "2":
                self._return_book_screen.display()

            elif choice == "3":
                self._my_borrowings_screen.display(
                    active_only=True
                )

            elif choice == "4":
                self._my_borrowings_screen.display(
                    active_only=False
                )

            elif choice == "0":
                logger.info("Borrowing menu exited")
                return

            else:
                logger.warning("Invalid borrowing menu choice: %s", choice)
                print("❌ Invalid choice.")