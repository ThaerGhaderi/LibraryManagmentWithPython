import logging
from getpass import getpass

from Services.auth_service import AuthService
from auth.exceptions import AuthError


logger = logging.getLogger(__name__)


class LoginScreen:

    def __init__(self, auth_service: AuthService) -> None:
        self.auth_service = auth_service

    def run(self) -> bool:
        print("\n" + "=" * 40)
        print("              LOGIN")
        print("=" * 40)

        username = input("Username: ").strip()
        password = getpass("Password: ")

        try:
            user = self.auth_service.login(
                username=username,
                password=password,
            )

            print("\n✅ Login successful.")
            print(f"Welcome back, {user.full_name}!")
            print(f"Role: {user.role.value}")
            logger.info(
                "UI login success: id=%s username=%s",
                user.id_user,
                user.username,
            )

            return True

        except AuthError as exc:
            logger.warning("UI login failed for username=%s: %s", username, exc)
            print(f"\n❌ {exc}")
            return False

        except ValueError as exc:
            logger.warning("UI login validation error for username=%s: %s", username, exc)
            print(f"\n❌ {exc}")
            return False