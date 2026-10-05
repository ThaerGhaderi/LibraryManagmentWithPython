import logging

from Services.report_service import ReportService


logger = logging.getLogger(__name__)


class LibraryStatisticsScreen:

    def __init__(
        self,
        report_service: ReportService,
    ) -> None:

        self.report_service = report_service

    def display(self) -> None:

        try:
            report = self.report_service.generate_report()

        except Exception as exc:
            logger.exception("UI library statistics report failed")
            print(f"❌ Failed to generate report: {exc}")
            return

        books = report["books"]
        users = report["users"]
        borrowings = report["borrowings"]
        rankings = report["rankings"]

        print("\n")
        print("=" * 60)
        logger.info("UI library statistics report displayed")
        print("                LIBRARY STATISTICS")
        print("=" * 60)

        print(f"Report Date: {report['generated_at']}")

        print("\n📚 BOOKS")
        print("-" * 60)
        print(f"Total Books       : {books['total']}")
        print(f"Available Books   : {books['available']}")
        print(f"Borrowed Books    : {books['borrowed']}")

        print("\n👥 USERS")
        print("-" * 60)
        print(f"Total Users       : {users['total']}")
        print(f"Members           : {users['members']}")
        print(f"Librarians        : {users['librarians']}")

        print("\n📖 BORROWINGS")
        print("-" * 60)
        print(f"Total Borrowings  : {borrowings['total']}")
        print(f"Active             : {borrowings['active']}")
        print(f"Returned           : {borrowings['returned']}")
        print(f"Overdue            : {borrowings['overdue']}")

        print(
            f"Total Fines       : "
            f"${borrowings['total_fines']:.2f}"
        )

        print(
            f"Average Duration  : "
            f"{borrowings['average_duration']:.2f} days"
        )

        self._display_most_borrowed_books(
            rankings["most_borrowed_books"]
        )

        self._display_most_active_users(
            rankings["most_active_users"]
        )

        print("=" * 60)

    @staticmethod
    def _display_most_borrowed_books(
        books: list[dict],
    ) -> None:

        print("\n🏆 MOST BORROWED BOOKS")
        print("-" * 60)

        if not books:
            logger.info("UI most borrowed books section empty")
            print("No borrowing data available.")
            return

        for index, book in enumerate(
            books,
            start=1,
        ):
            print(
                f"{index}. "
                f"{book['title']} - "
                f"{book['author']} "
                f"({book['borrow_count']} borrowings)"
            )

    @staticmethod
    def _display_most_active_users(
        users: list[dict],
    ) -> None:

        print("\n👑 MOST ACTIVE USERS")
        print("-" * 60)

        if not users:
            logger.info("UI most active users section empty")
            print("No borrowing data available.")
            return

        for index, user in enumerate(
            users,
            start=1,
        ):
            print(
                f"{index}. "
                f"{user['full_name']} "
                f"(@{user['username']}) - "
                f"{user['borrow_count']} borrowings"
            )