import logging

from auth.session import Session
from Services.auth_service import AuthService
from Services.book_service import BookService
from Services.borrowing_service import BorrowingService
from Services.member_service import MemberService
from Services.report_service import ReportService
from Services.user_service import UserService
from UI.auth.auth_menu import AuthMenu
from UI.menus.main_menu import MainMenu
from repositories.book_repository import BookRepository
from repositories.borrowing_repository import BorrowingRepository
from repositories.user_repository import UserRepository
from utils.logger import setup_logging


logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    logger.info("Application starting")

    session = Session()

    auth_service = AuthService(
        session=session
    )

    user_service = UserService(
        session=session
    )

    borrowing_service = BorrowingService(
        session=session,
        book_repository=BookRepository(),
        borrowing_repository=BorrowingRepository(),
    )


    book_repository = BookRepository()
    user_repository = UserRepository()
    borrowing_repository = BorrowingRepository()
    
    
    book_service = BookService(
        repository=book_repository,
        session=session,
    )


    report_service = ReportService(
     session=session,
     book_repository=book_repository,
     user_repository=user_repository,
     borrowing_repository=borrowing_repository,
    )
    member_service = MemberService(
     session=session,
     user_repository=UserRepository(),
     borrowing_repository=BorrowingRepository(),
    )
     
    auth_menu = AuthMenu(
        auth_service
    )

    if not auth_menu.run():
        return

    main_menu = MainMenu(
        session=session,
        auth_service=auth_service,
        user_service=user_service,
        borrowing_service=borrowing_service,
        book_service=book_service,
        report_service=report_service,
        member_service=member_service,
    )

    main_menu.run()
    logger.info("Application finished")


if __name__ == "__main__":
    main()