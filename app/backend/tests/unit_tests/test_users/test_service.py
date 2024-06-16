import pytest

from app.backend.users.service import UsersDAO


@pytest.mark.parametrize("user_id, email, exists", [
    (1, "test@test.com", True),
    (2, "artem@example.com", True),
    (4, "notexistinguser@gmailc.com", False)
])
async def test_get_one_or_none_user(user_id, email, exists):
    user = await UsersDAO.get_one_or_none(id=user_id)

    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user

