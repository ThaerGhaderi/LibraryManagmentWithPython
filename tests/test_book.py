import pytest

from Models.book import Book


def test_book_creation():
    book = Book(
        title="Clean Code",
        author="Robert Martin",
        year=2008,
        classification=["Programming", "Software"],
        publication_site="Pearson",
    )

    assert book.title == "Clean Code"
    assert book.author == "Robert Martin"
    assert book.year == 2008
    assert book.available is True
    assert book.classification == [
        "Programming",
        "Software",
    ]


def test_book_id_generation():
    book1 = Book(
        "Book One",
        "Author One",
        2020,
        "AI",
    )

    book2 = Book(
        "Book Two",
        "Author Two",
        2021,
        "AI",
    )

    assert book2.id_book == book1.id_book + 1


def test_book_id_counter_sync_after_loading():
    Book(
        "Book One",
        "Author One",
        2020,
        "AI",
        id_book=10,
    )

    book = Book(
        "Book Two",
        "Author Two",
        2021,
        "AI",
    )

    assert book.id_book == 11


def test_book_serialization_round_trip():
    book = Book(
        title="Python Crash Course",
        author="Eric Matthes",
        year=2019,
        classification=["Python", "Programming"],
        publication_site="No Starch Press",
    )

    data = book.to_dict()
    restored = Book.from_dict(data)

    assert restored.id_book == book.id_book
    assert restored.title == book.title
    assert restored.author == book.author
    assert restored.year == book.year
    assert restored.classification == book.classification
    assert restored.available == book.available
    assert restored.publication_site == book.publication_site


def test_update_available():
    book = Book(
        "Test Book",
        "Test Author",
        2024,
        "AI",
    )

    book.update_available(False)

    assert book.available is False

    book.update_available(True)

    assert book.available is True


def test_book_validation():
    with pytest.raises(ValueError):
        Book(
            "",
            "Author",
            2024,
            "AI",
        )

    with pytest.raises(ValueError):
        Book(
            "Title",
            "",
            2024,
            "AI",
        )

    with pytest.raises(ValueError):
        Book(
            "Title",
            "Author",
            0,
            "AI",
        )

    with pytest.raises(ValueError):
        Book(
            "Title",
            "Author",
            2024,
            [],
        )