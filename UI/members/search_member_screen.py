import logging

from Services.member_service import MemberService


logger = logging.getLogger(__name__)


class SearchMemberScreen:

    def __init__(
        self,
        member_service: MemberService,
    ) -> None:

        self.member_service = member_service

    def display(self) -> None:

        query = input(
            "Search by name or username: "
        ).strip()

        members = self.member_service.search_members(
            query
        )

        print("\n--- SEARCH RESULTS ---")

        if not members:
            logger.info("UI member search returned no results")
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
                f"{member.full_name} | "
                f"@{member.username} | "
                f"{status}"
            )

        logger.info("UI member search displayed results: count=%s", len(members))