import logging

from Services.member_service import MemberService


logger = logging.getLogger(__name__)


class ListMembersScreen:

    def __init__(
        self,
        member_service: MemberService,
    ) -> None:

        self.member_service = member_service

    def display(self) -> None:

        print("\n--- MEMBERS ---")

        members = self.member_service.get_all_members()

        if not members:
            logger.info("UI members list returned no results")
            print("No members found.")
            return

        for member in members:

            status = (
                "Active"
                if member.active
                else "Inactive"
            )

            print(
                f"ID: {member.id_user} | "
                f"Name: {member.full_name} | "
                f"Username: @{member.username} | "
                f"Status: {status}"
            )

        logger.info("UI members list displayed: count=%s", len(members))