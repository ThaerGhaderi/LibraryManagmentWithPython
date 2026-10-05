import logging

from Services.member_service import MemberService


logger = logging.getLogger(__name__)


class MemberDetailsScreen:

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

            borrowings = (
                self.member_service
                .get_member_borrowings(user_id)
            )

            active_count = sum(
                1
                for borrowing in borrowings
                if borrowing.is_active()
            )

            print("\n" + "=" * 40)
            print("           MEMBER DETAILS")
            print("=" * 40)

            print(f"ID        : {member.id_user}")
            print(f"Name      : {member.full_name}")
            print(f"Username  : @{member.username}")
            print(f"Role      : {member.role.value}")
            print(
                f"Status    : "
                f"{'Active' if member.active else 'Inactive'}"
            )

            print(
                f"Borrowings: {len(borrowings)}"
            )

            print(
                f"Active    : {active_count}"
            )

            print("=" * 40)
            logger.info(
                "UI member details displayed: id=%s borrowings=%s active_borrowings=%s",
                member.id_user,
                len(borrowings),
                active_count,
            )

        except ValueError:
            logger.warning("UI member details validation error: invalid member id")
            print("❌ Invalid member ID.")

        except Exception as exc:
            logger.warning("UI member details failed: %s", exc)
            print(f"❌ {exc}")