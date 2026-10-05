import logging

from Services.report_service import ReportService

from UI.reports.library_statistics_screen import (
    LibraryStatisticsScreen,
)

from UI.reports.borrowing_report_screen import (
    BorrowingReportScreen,
)


logger = logging.getLogger(__name__)


class ReportsMenu:

    def __init__(
        self,
        report_service: ReportService,
    ) -> None:

        self.report_service = report_service

        self.statistics_screen = (
            LibraryStatisticsScreen(
                report_service
            )
        )

        self.borrowing_report_screen = (
            BorrowingReportScreen(
                report_service
            )
        )

    def display_menu(self) -> None:

        print("\n" + "=" * 45)
        print("             REPORTS MENU")
        print("=" * 45)

        print("1. Library Statistics")
        print("2. Borrowing Reports")
        print("0. Back")

    def run(self) -> None:

        while self.report_service.session.is_authenticated:

            self.display_menu()

            choice = input(
                "Enter your choice: "
            ).strip()

            if choice == "1":

                self.statistics_screen.display()

            elif choice == "2":

                self.borrowing_report_screen.display()

            elif choice == "0":
                logger.info("Reports menu exited")
                return

            else:
                logger.warning("Invalid reports menu choice: %s", choice)
                print("❌ Invalid choice.")