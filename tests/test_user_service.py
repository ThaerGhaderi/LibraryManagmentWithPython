from auth.password_hasher import PasswordHasher


def test_update_full_name_persists(
    app,
    member_user,
):

    app.session.login(member_user)

    updated = app.user_service.update_full_name(
        "New Full Name"
    )

    assert updated.full_name == "New Full Name"

    users = app.user_repository.get_all()

    stored_user = next(
        user
        for user in users
        if user.id_user == member_user.id_user
    )

    assert stored_user.full_name == "New Full Name"
    assert (
        app.session.current_user.full_name
        == "New Full Name"
    )


def test_change_password_persists(
    app,
):

    old_password = "OldPassword123"
    new_password = "NewPassword456"

    old_hash, old_salt = (
        PasswordHasher.hash_password(
            old_password
        )
    )

    from Models.user import User

    user = User(
        full_name="Thaer",
        username="thaer",
        password_hash=old_hash,
        salt=old_salt,
    )

    app.user_repository.save_all([user])
    app.session.login(user)

    app.user_service.change_password(
        current_password=old_password,
        new_password=new_password,
        confirm_password=new_password,
    )

    users = app.user_repository.get_all()

    stored_user = users[0]

    assert PasswordHasher.verify_password(
        new_password,
        stored_user.password_hash,
        stored_user.salt,
    )

    assert not PasswordHasher.verify_password(
        old_password,
        stored_user.password_hash,
        stored_user.salt,
    )

    assert (
        app.session.current_user.password_hash
        == stored_user.password_hash
    )


def test_wrong_current_password_rejected(
    app,
    member_user,
):

    app.session.login(member_user)

    from pytest import raises

    with raises(ValueError):

        app.user_service.change_password(
            current_password="WrongPassword123",
            new_password="NewPassword456",
            confirm_password="NewPassword456",
        )


def test_password_confirmation_required(
    app,
    member_user,
):

    app.session.login(member_user)

    from pytest import raises

    with raises(ValueError):

        app.user_service.change_password(
            current_password="Password123",
            new_password="NewPassword456",
            confirm_password="DifferentPassword",
        )