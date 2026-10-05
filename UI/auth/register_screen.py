import logging
from getpass import getpass

from Services.auth_service import AuthService
from auth.exceptions import AuthError


logger = logging.getLogger(__name__)


class RegisterScreen:

    def __init__(self, auth_service: AuthService) -> None:
        self.auth_service = auth_service

    def run(self) -> bool:
        print("\n" + "=" * 40)
        print("             REGISTER")
        print("=" * 40)

        full_name = input("Full name: ").strip()
        username = input("Username: ").strip()

        password = getpass("Password: ")
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            print("\n❌ Passwords do not match.")
            return False

        try:
            user = self.auth_service.register(
                full_name=full_name,
                username=username,
                password=password,
            )

            print("\n✅ Account created successfully.")
            print(f"Welcome, {user.full_name}!")
            print(f"Username: {user.username}")
            print(f"Role: {user.role.value}")
            logger.info(
                "UI registration success: id=%s username=%s role=%s",
                user.id_user,
                user.username,
                user.role.value,
            )

            return True

        except AuthError as exc:
            logger.warning("UI registration failed for username=%s: %s", username, exc)
            print(f"\n❌ {exc}")
            return False

        except ValueError as exc:
            logger.warning("UI registration validation error for username=%s: %s", username, exc)
            print(f"\n❌ {exc}")
            return False