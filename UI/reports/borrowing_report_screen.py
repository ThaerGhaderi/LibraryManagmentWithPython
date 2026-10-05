import logging

from Services.report_service import ReportService


logger = logging.getLogger(__name__)


class BorrowingReportScreen:

    def __init__(
        self,
        report_service: ReportService,
    ) -> None:

        self.report_service = report_service

    def display(self) -> None:

        while True:

            print("\n" + "=" * 45)
            print("          BORROWING REPORTS")
            print("=" * 45)

            print("1. Active Borrowings")
            print("2. Overdue Borrowings")
            print("3. Returned Borrowings")
            print("0. Back")

            choice = input(
                "Choose an option: "
            ).strip()

            if choice == "1":
                self._show_active()

            elif choice == "2":
                self._show_overdue()

            elif choice == "3":
                self._show_returned()

            elif choice == "0":
                logger.info("Borrowing reports screen exited")
                return

            else:
                logger.warning("Invalid borrowing reports choice: %s", choice)
                print("❌ Invalid choice.")

    def _show_active(self) -> None:

        borrowings = (
            self.report_service
            .get_active_borrowings()
        )

        print("\n--- ACTIVE BORROWINGS ---")

        if not borrowings:
            logger.info("UI active borrowings section empty")
            print("No active borrowings.")
            return

        for borrowing in borrowings:

            print(
                f"Borrowing ID : "
                f"{borrowing.id_borrowing}"
            )

            print(
                f"Book ID      : "
                f"{borrowing.book_id}"
            )

            print(
                f"User ID      : "
                f"{borrowing.user_id}"
            )

            print(
                f"Start Date   : "
                f"{borrowing.start_date}"
            )

            print(
                f"End Date     : "
                f"{borrowing.end_date}"
            )

            print("-" * 35)

    def _show_overdue(self) -> None:

        borrowings = (
            self.report_service
            .get_overdue_borrowings()
        )

        print("\n--- OVERDUE BORROWINGS ---")

        if not borrowings:
            logger.info("UI overdue borrowings section empty")
            print("✅ No overdue borrowings.")
            return

        for borrowing in borrowings:

            overdue_days = (
                self._calculate_overdue_days(
                    borrowing.end_date
                )
            )

            print(
                f"Borrowing ID : "
                f"{borrowing.id_borrowing}"
            )

            print(
                f"Book ID      : "
                f"{borrowing.book_id}"
            )

            print(
                f"User ID      : "
                f"{borrowing.user_id}"
            )

            print(
                f"Due Date     : "
                f"{borrowing.end_date}"
            )

            print(
                f"Overdue      : "
                f"{overdue_days} days"
            )

            print("-" * 35)

    def _show_returned(self) -> None:

        borrowings = (
            self.report_service
            .get_returned_borrowings()
        )

        print("\n--- RETURNED BORROWINGS ---")

        if not borrowings:
            logger.info("UI returned borrowings section empty")
            print("No returned borrowings.")
            return

        for borrowing in borrowings:

            print(
                f"Borrowing ID : "
                f"{borrowing.id_borrowing}"
            )

            print(
                f"Book ID      : "
                f"{borrowing.book_id}"
            )

            print(
                f"User ID      : "
                f"{borrowing.user_id}"
            )

            print(
                f"Start Date   : "
                f"{borrowing.start_date}"
            )

            print(
                f"Returned At  : "
                f"{borrowing.returned_at}"
            )

            print(
                f"Fine         : "
                f"${borrowing.fine:.2f}"
            )

            print("-" * 35)

    @staticmethod
    def _calculate_overdue_days(
        end_date,
    ) -> int:

        return (
            __import__("datetime")
            .date.today()
            - end_date
        ).days