import pytest

from Models.user import User, UserRole


def test_user_creation():
    user = User(
        full_name="Thaer Ahmad",
        username="THAER",
        password_hash="hash",
        salt="salt",
    )

    assert user.full_name == "Thaer Ahmad"
    assert user.username == "thaer"
    assert user.role == UserRole.MEMBER
    assert user.active is True


def test_user_role():
    user = User(
        full_name="Admin",
        username="admin",
        password_hash="hash",
        salt="salt",
        role=UserRole.LIBRARIAN,
    )

    assert user.role == UserRole.LIBRARIAN


def test_user_id_generation():
    user1 = User(
        "User One",
        "user1",
        "hash",
        "salt",
    )

    user2 = User(
        "User Two",
        "user2",
        "hash",
        "salt",
    )

    assert user2.id_user == user1.id_user + 1


def test_user_serialization_round_trip():
    user = User(
        full_name="Thaer Ahmad",
        username="thaer",
        password_hash="hash123",
        salt="salt123",
        role=UserRole.LIBRARIAN,
        active=False,
    )

    data = user.to_dict()
    restored = User.from_dict(data)

    assert restored.id_user == user.id_user
    assert restored.full_name == user.full_name
    assert restored.username == user.username
    assert restored.password_hash == user.password_hash
    assert restored.salt == user.salt
    assert restored.role == user.role
    assert restored.active is False


def test_user_activate_deactivate():
    user = User(
        "Test",
        "test",
        "hash",
        "salt",
    )

    user.deactivate()

    assert user.active is False

    user.activate()

    assert user.active is True


def test_user_update_full_name():
    user = User(
        "Old Name",
        "test",
        "hash",
        "salt",
    )

    user.update_full_name("New Name")

    assert user.full_name == "New Name"

    with pytest.raises(ValueError):
        user.update_full_name("")


def test_invalid_role():
    with pytest.raises(ValueError):
        User(
            "Test",
            "test",
            "hash",
            "salt",
            role="invalid-role",
        )


def test_user_validation():
    with pytest.raises(ValueError):
        User(
            "",
            "test",
            "hash",
            "salt",
        )

    with pytest.raises(ValueError):
        User(
            "Test",
            "",
            "hash",
            "salt",
        )

    with pytest.raises(ValueError):
        User(
            "Test",
            "test",
            "",
            "salt",
        )

    with pytest.raises(ValueError):
        User(
            "Test",
            "test",
            "hash",
            "",
        )