class Book:

    _last_id = 0

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        classification,
        available: bool = True,
        publication_site: str | None = None,
        id_book: int | None = None,
    ) -> None:

        title = title.strip()
        author = author.strip()

        if not title:
            raise ValueError("Book title cannot be empty.")

        if not author:
            raise ValueError("Book author cannot be empty.")

        if not isinstance(year, int):
            raise TypeError("Year must be an integer.")

        if year <= 0:
            raise ValueError("Year must be a positive integer.")

        if isinstance(classification, str):
            classification = classification.split(",")

        classification = [
            item.strip()
            for item in classification
            if str(item).strip()
        ]

        if not classification:
            raise ValueError(
                "Book must have at least one classification."
            )

        if not isinstance(available, bool):
            raise TypeError("available must be a bool.")

        if id_book is None:
            Book._last_id += 1
            self._id_book = Book._last_id
        else:
            if id_book <= 0:
                raise ValueError(
                    "id_book must be a positive integer."
                )

            self._id_book = id_book

            if id_book > Book._last_id:
                Book._last_id = id_book

        self._title = title
        self._author = author
        self._year = year
        self._classification = classification
        self._available = available
        self._publication_site = (
            publication_site.strip()
            if publication_site
            else None
        )

  
    @property
    def id_book(self) -> int:
        return self._id_book

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    @property
    def year(self) -> int:
        return self._year

    @property
    def classification(self) -> list[str]:
        return list(self._classification)

    @property
    def available(self) -> bool:
        return self._available

    @property
    def publication_site(self) -> str | None:
        return self._publication_site


    def update_available(self, available: bool) -> None:
        if not isinstance(available, bool):
            raise TypeError("available must be a bool.")

        self._available = available

    def update_details(
        self,
        title: str | None = None,
        author: str | None = None,
        year: int | None = None,
        classification=None,
        publication_site: str | None = None,
    ) -> None:

        if title is not None:
            title = title.strip()

            if not title:
                raise ValueError(
                    "Book title cannot be empty."
                )

            self._title = title

        if author is not None:
            author = author.strip()

            if not author:
                raise ValueError(
                    "Book author cannot be empty."
                )

            self._author = author

        if year is not None:
            if not isinstance(year, int) or year <= 0:
                raise ValueError(
                    "Year must be a positive integer."
                )

            self._year = year

        if classification is not None:

            if isinstance(classification, str):
                classification = classification.split(",")

            classification = [
                item.strip()
                for item in classification
                if str(item).strip()
            ]

            if not classification:
                raise ValueError(
                    "Book must have at least one classification."
                )

            self._classification = classification

        if publication_site is not None:
            publication_site = publication_site.strip()

            self._publication_site = (
                publication_site
                if publication_site
                else None
            )

    def to_dict(self) -> dict:
        return {
            "id_book": self._id_book,
            "title": self._title,
            "author": self._author,
            "year": self._year,
            "classification": self._classification,
            "available": self._available,
            "publication_site": self._publication_site,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":

        publication_site = data.get(
            "publication_site",
            data.get("Publication_Site")
        )

        return cls(
            id_book=data["id_book"],
            title=data["title"],
            author=data["author"],
            year=int(data["year"]),
            classification=data["classification"],
            available=data.get("available", True),
            publication_site=publication_site,
        )

    def __str__(self) -> str:

        site = (
            self._publication_site
            if self._publication_site
            else "undefined"
        )

        status = (
            "Available"
            if self._available
            else "Borrowed"
        )

        return (
            f"Book #{self._id_book} | "
            f"{self._title} | "
            f"{self._author} | "
            f"{self._year} | "
            f"{self._classification} | "
            f"{status} | "
            f"Site: {site}"
        )