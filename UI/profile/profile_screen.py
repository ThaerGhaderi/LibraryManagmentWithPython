import logging
from getpass import getpass
from Services.user_service import UserService
from auth.exceptions import AuthError


logger = logging.getLogger(__name__)


class ProfileScreen:
    def __init__(self , user_service: UserService)->None:
        self.user_service = user_service

    def run(self)->None:
          while True:

            print("\n" + "=" * 40)
            print("              MY PROFILE")
            print("=" * 40)

            self._display_profile_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.show_profile()

            elif choice == "2":
                self.change_full_name()

            elif choice == "3":
                self.change_password()

            elif choice == "0":
                logger.info("Profile screen exited")
                return

            else:
                logger.warning("Invalid profile menu choice: %s", choice)
                print("❌ Invalid choice.")

    @staticmethod
    def _display_profile_menu() -> None:
        print("1. View Profile")
        print("2. Change Full Name")
        print("3. Change Password")
        print("0. Back")


    def show_profile(self)->None:
        user = self.user_service.get_current_user()

        print("\n---------- PROFILE ----------")
        print(f"ID       : {user.id_user}")
        print(f"Name     : {user.full_name}")
        print(f"Username : {user.username}")
        print(f"Role     : {user.role.value}")
        print("-----------------------------")
        logger.info("Profile viewed: id=%s username=%s", user.id_user, user.username)


    def change_full_name(self)->None:
         print("\n========== CHANGE NAME ==========")

         full_name = input("New full name: ").strip()


         try:
            user = self.user_service.update_full_name(
                 full_name=full_name
            )

            print(
                f"✅ Name updated successfully. "
                f"Welcome, {user.full_name}"
            )
            logger.info(
                "Profile full name changed: id=%s username=%s",
                user.id_user,
                user.username,
            )
         except (AuthError, ValueError) as exc:
            logger.warning("Profile full name change failed: %s", exc)
            print(f"❌ {exc}")

    def change_password(self) -> None:
         print("\n========== CHANGE PASSWORD ==========")

         current_password = getpass(
            "Current password: "
          )

         new_password = getpass(
            "New password: "
          )

         confirm_password = getpass(
            "Confirm new password: "
          )
         try:
                self.user_service.change_password(
                    current_password=current_password,
                    new_password=new_password,
                    confirm_password=confirm_password,
                )

                print("✅ Password changed successfully.")
                logger.info("Profile password changed successfully")

         except (AuthError, ValueError) as exc:
            logger.warning("Profile password change failed: %s", exc)
            print(f"❌ {exc}")
