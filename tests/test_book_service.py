import pytest

from Models.book import Book

from Services.book_service import (
    BookAlreadyExistsError,
    BookError,
    BookPermissionError,
    BookService,
)


def create_book(
    title="Clean Code",
    author="Robert Martin",
    year=2008,
    classification="Programming",
):
    return Book(
        title=title,
        author=author,
        year=year,
        classification=classification,
    )


def test_add_book(app, librarian_user):

    app.session.login(librarian_user)

    book = create_book()

    added = app.book_service.add_book(book)

    assert added.id_book == book.id_book

    books = app.book_repository.get_all()

    assert len(books) == 1
    assert books[0].title == "Clean Code"


def test_duplicate_book_rejected(
    app,
    librarian_user,
):

    app.session.login(librarian_user)

    app.book_service.add_book(
        create_book()
    )

    with pytest.raises(BookAlreadyExistsError):

        app.book_service.add_book(
            create_book()
        )


def test_find_book_by_id(app, librarian_user):

    app.session.login(librarian_user)

    book = app.book_service.add_book(
        create_book()
    )

    found = app.book_service.find_book_by_id(
        book.id_book
    )

    assert found is not None
    assert found.id_book == book.id_book


def test_search_by_title(app, librarian_user):

    app.session.login(librarian_user)

    app.book_service.add_book(
        create_book(
            title="Python Crash Course"
        )
    )

    app.book_service.add_book(
        create_book(
            title="Clean Code",
            author="Robert Martin",
        )
    )

    results = app.book_service.search_by_title(
        "python"
    )

    assert len(results) == 1
    assert results[0].title == "Python Crash Course"


def test_search_by_author(app, librarian_user):

    app.session.login(librarian_user)

    app.book_service.add_book(
        create_book(
            author="Eric Matthes"
        )
    )

    results = app.book_service.search_by_author(
        "eric"
    )

    assert len(results) == 1
    assert results[0].author == "Eric Matthes"


def test_search_by_classification(
    app,
    librarian_user,
):

    app.session.login(librarian_user)

    app.book_service.add_book(
        create_book(
            classification=[
                "AI",
                "Machine Learning",
            ]
        )
    )

    results = (
        app.book_service
        .search_by_classification("machine")
    )

    assert len(results) == 1


def test_update_book(app, librarian_user):

    app.session.login(librarian_user)

    book = app.book_service.add_book(
        create_book()
    )

    updated = app.book_service.update_book(
        book.id_book,
        title="Clean Architecture",
        year=2017,
    )

    assert updated.title == "Clean Architecture"
    assert updated.year == 2017


def test_delete_book(app, librarian_user):

    app.session.login(librarian_user)

    book = app.book_service.add_book(
        create_book()
    )

    deleted = app.book_service.delete_book(
        book.id_book
    )

    assert deleted.id_book == book.id_book
    assert app.book_service.get_all_books() == []


def test_available_and_borrowed_books(
    app,
    librarian_user,
):

    app.session.login(librarian_user)

    book1 = app.book_service.add_book(
        create_book("Book 1")
    )

    book2 = app.book_service.add_book(
        create_book(
            "Book 2",
            author="Author 2",
        )
    )

    book2.update_available(False)

    app.book_repository.save_all(
        [book1, book2]
    )

    available = (
        app.book_service
        .get_available_books()
    )

    borrowed = (
        app.book_service
        .get_borrowed_books()
    )

    assert len(available) == 1
    assert len(borrowed) == 1


def test_member_cannot_add_book(
    app,
    member_user,
):

    app.session.login(member_user)

    with pytest.raises(BookPermissionError):

        app.book_service.add_book(
            create_book()
        )


def test_borrowed_book_cannot_be_deleted(
    app,
    librarian_user,
):

    app.session.login(librarian_user)

    book = app.book_service.add_book(
        create_book()
    )

    book.update_available(False)

    app.book_repository.save_all([book])

    with pytest.raises(BookError):

        app.book_service.delete_book(
            book.id_book
        )