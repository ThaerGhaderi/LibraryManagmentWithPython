import logging

from Services.member_service import (
    MemberService,
    MemberError,
    MemberNotFoundError,
    MemberHasActiveBorrowingsError,
)


logger = logging.getLogger(__name__)


class MemberStatusScreen:

    def __init__(
        self,
        member_service: MemberService,
    ) -> None:

        self.member_service = member_service

    def display(self) -> None:

        try:
            user_id = int(
                input("Member ID: ")
            )

            member = self.member_service.get_member_by_id(
                user_id
            )

            print(f"\n{member}")

            print("\n1. Deactivate")
            print("2. Activate")
            print("0. Cancel")

            choice = input("Choose: ").strip()

            if choice == "1":

                self.member_service.deactivate_member(
                    user_id
                )

                print(
                    "✅ Member deactivated successfully."
                )
                logger.info("UI member deactivated: id=%s", user_id)

            elif choice == "2":

                self.member_service.activate_member(
                    user_id
                )

                print(
                    "✅ Member activated successfully."
                )
                logger.info("UI member activated: id=%s", user_id)

            elif choice == "0":
                return

            else:
                logger.warning("Invalid member status choice: %s", choice)
                print("❌ Invalid choice.")

        except ValueError:
            logger.warning("UI member status validation error: invalid member id")
            print("❌ Invalid member ID.")

        except (
            MemberNotFoundError,
            MemberHasActiveBorrowingsError,
            MemberError,
        ) as exc:
            logger.warning("UI member status failed: %s", exc)
            print(f"❌ {exc}")