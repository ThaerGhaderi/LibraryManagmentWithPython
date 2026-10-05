import logging

from Services.auth_service import AuthService
from UI.auth.login_screen import LoginScreen
from UI.auth.register_screen import RegisterScreen


logger = logging.getLogger(__name__)


class AuthMenu:

    def __init__(self, auth_service: AuthService) -> None:
        self.auth_service = auth_service

        self.register_screen = RegisterScreen(
            auth_service
        )

        self.login_screen = LoginScreen(
            auth_service
        )

    def run(self) -> bool:
        """
        Display the authentication menu.

        Returns:
            True  -> user authenticated successfully.
            False -> user chose to exit.
        """

        while not self.auth_service.is_authenticated():

            self._display_menu()

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.register_screen.run()

            elif choice == "2":
                self.login_screen.run()

            elif choice == "0":
                print("\nGoodbye 👋")
                logger.info("Auth menu exited by user")
                return False

            else:
                logger.warning("Invalid auth menu choice: %s", choice)
                print("\n❌ Invalid choice.")

        return True

    @staticmethod
    def _display_menu() -> None:
        print("\n" + "=" * 40)
        print("       LIBRARY MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Register")
        print("2. Login")
        print("0. Exit")
        print("=" * 40)