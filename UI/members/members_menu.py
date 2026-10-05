import logging

from Services.member_service import MemberService

from UI.members.list_members_screen import (
    ListMembersScreen,
)

from UI.members.search_member_screen import (
    SearchMemberScreen,
)

from UI.members.member_details_screen import (
    MemberDetailsScreen,
)

from UI.members.member_status_screen import (
    MemberStatusScreen,
)


logger = logging.getLogger(__name__)


class MembersMenu:

    def __init__(
        self,
        member_service: MemberService,
    ) -> None:

        self.member_service = member_service

        self.list_screen = ListMembersScreen(
            member_service
        )

        self.search_screen = SearchMemberScreen(
            member_service
        )

        self.details_screen = MemberDetailsScreen(
            member_service
        )

        self.status_screen = MemberStatusScreen(
            member_service
        )

    def display_menu(self) -> None:

        print("\n" + "=" * 40)
        print("           MEMBERS MANAGEMENT")
        print("=" * 40)

        print("1. List Members")
        print("2. Search Member")
        print("3. Member Details")
        print("4. Activate / Deactivate Member")
        print("0. Back")

    def run(self) -> None:

        while self.member_service.session.is_authenticated:

            self.display_menu()

            choice = input(
                "Enter your choice: "
            ).strip()

            if choice == "1":

                self.list_screen.display()

            elif choice == "2":

                self.search_screen.display()

            elif choice == "3":

                self.details_screen.display()

            elif choice == "4":

                self.status_screen.display()

            elif choice == "0":
                logger.info("Members menu exited")
                return

            else:
                logger.warning("Invalid members menu choice: %s", choice)
                print("❌ Invalid choice.")