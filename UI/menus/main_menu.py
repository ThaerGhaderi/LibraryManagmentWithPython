import logging

from auth.session import Session
from Models.user import UserRole

from Services.auth_service import AuthService
from Services.user_service import UserService
from Services.borrowing_service import BorrowingService

from UI.profile.profile_screen import ProfileScreen
from UI.borrowing.borrowing_menu import BorrowingMenu

from UI.books.books_menu import BooksMenu
from Services.book_service import BookService

from UI.reports.reports_menu import ReportsMenu
from Services.report_service import ReportService

from UI.members.members_menu import MembersMenu
from Services.member_service import MemberService


logger = logging.getLogger(__name__)


class MainMenu:

    def __init__(
        self,
        session: Session,
        auth_service: AuthService,
        user_service: UserService,
        borrowing_service: BorrowingService,
        book_service: BookService,
        report_service: ReportService,
        member_service: MemberService,
    ) -> None:

        self.session = session
        self.auth_service = auth_service
        self.user_service = user_service
        self.borrowing_service = borrowing_service
        self.book_service = book_service
        self.report_service = report_service
        self.member_service = member_service

        self.profile_screen = ProfileScreen(
            user_service=user_service
        )

        self.borrowing_menu = BorrowingMenu(
            borrowing_service=borrowing_service
        )


        self.books_menu = BooksMenu(
            book_service=book_service
        )


        self.reports_menu = ReportsMenu(
            report_service
        )

        self.members_menu = MembersMenu(
            member_service=member_service
        )
    def welcome_message(self) -> None:

        user = self.session.require_authentication()

        print("\n" + "=" * 40)
        print("       LIBRARY MANAGEMENT SYSTEM")
        print("=" * 40)
        print(f"Welcome, {user.username} 👋")
        print(f"Role: {user.role.value}")
        print("=" * 40)

    def display_menu(self) -> None:

        user = self.session.require_authentication()

        if user.role == UserRole.MEMBER:

            print("1. Books")
            print("2. Borrowing")
            print("3. My Profile")
            print("4. Logout")
            print("0. Exit")

        elif user.role == UserRole.LIBRARIAN:

            print("1. Books")
            print("2. Members")
            print("3. Borrowing")
            print("4. Reports")
            print("5. My Profile")
            print("6. Logout")
            print("0. Exit")

    def run(self) -> bool:

        while self.session.is_authenticated:

            self.welcome_message()
            self.display_menu()

            choice = input(
                "Enter your choice: "
            ).strip()

            user = self.session.require_authentication()

          

            if user.role == UserRole.MEMBER:

                if choice == "1":
                     self.books_menu.run()
                elif choice == "2":
                    self.borrowing_menu.run()

                elif choice == "3":
                    self.profile_screen.run()

                elif choice == "4":
                    self.auth_service.logout()
                    print("✅ Logged out successfully.")
                    logger.info("Main menu logout selected by member")

                elif choice == "0":
                    logger.info("Main menu exited by member")
                    return False

                else:
                    logger.warning("Invalid main menu choice for member: %s", choice)
                    print("❌ Invalid choice.")

         

            elif user.role == UserRole.LIBRARIAN:

                if choice == "1":
                     self.books_menu.run()

                elif choice == "2":
                    self.members_menu.run()
                elif choice == "3":
                    self.borrowing_menu.run()

                elif choice == "4":
                    self.reports_menu.run()
                elif choice == "5":
                    self.profile_screen.run()

                elif choice == "6":
                    self.auth_service.logout()
                    print("✅ Logged out successfully.")
                    logger.info("Main menu logout selected by librarian")

                elif choice == "0":
                    logger.info("Main menu exited by librarian")
                    return False

                else:
                    logger.warning("Invalid main menu choice for librarian: %s", choice)
                    print("❌ Invalid choice.")

        return True