import pytest

from Models.user import UserRole

from auth.exceptions import (
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
)

from auth.password_hasher import PasswordHasher


def test_register_first_user_becomes_librarian(app):

    user = app.auth_service.register(
        full_name="Thaer",
        username="thaer",
        password="Password123",
    )

    assert user.role == UserRole.LIBRARIAN
    assert user.username == "thaer"
    assert app.session.is_authenticated
    assert app.session.current_user.id_user == user.id_user


def test_second_user_becomes_member(app):

    app.auth_service.register(
        "First User",
        "first",
        "Password123",
    )

    app.auth_service.logout()

    second_user = app.auth_service.register(
        "Second User",
        "second",
        "Password123",
    )

    assert second_user.role == UserRole.MEMBER


def test_duplicate_username_is_rejected(app):

    app.auth_service.register(
        "Thaer",
        "thaer",
        "Password123",
    )

    app.auth_service.logout()

    with pytest.raises(UsernameAlreadyExistsError):

        app.auth_service.register(
            "Another",
            "THAER",
            "Password456",
        )


def test_login_success(app):

    user = app.auth_service.register(
        "Thaer",
        "thaer",
        "Password123",
    )

    app.auth_service.logout()

    logged_in_user = app.auth_service.login(
        "THAER",
        "Password123",
    )

    assert logged_in_user.id_user == user.id_user
    assert app.session.is_authenticated
    assert app.session.current_user.id_user == user.id_user


def test_wrong_password_rejected(app):

    app.auth_service.register(
        "Thaer",
        "thaer",
        "Password123",
    )

    app.auth_service.logout()

    with pytest.raises(InvalidCredentialsError):

        app.auth_service.login(
            "thaer",
            "WrongPassword",
        )


def test_wrong_username_rejected(app):

    with pytest.raises(InvalidCredentialsError):

        app.auth_service.login(
            "does_not_exist",
            "Password123",
        )


def test_logout(app):

    app.auth_service.register(
        "Thaer",
        "thaer",
        "Password123",
    )

    assert app.session.is_authenticated

    app.auth_service.logout()

    assert not app.session.is_authenticated
    assert app.session.current_user is None


def test_inactive_user_cannot_login(app):

    user = app.auth_service.register(
        "Thaer",
        "thaer",
        "Password123",
    )

    user.deactivate()

    users = app.user_repository.get_all()

    stored_user = next(
        user_item
        for user_item in users
        if user_item.id_user == user.id_user
    )

    stored_user.deactivate()

    app.user_repository.save_all(users)

    app.auth_service.logout()

    with pytest.raises(InvalidCredentialsError):

        app.auth_service.login(
            "thaer",
            "Password123",
        )


def test_password_hash_is_not_plaintext(app):

    user = app.auth_service.register(
        "Thaer",
        "thaer",
        "Password123",
    )

    assert user.password_hash != "Password123"
    assert user.salt