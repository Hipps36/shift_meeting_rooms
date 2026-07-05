import pytest

from fastapi_users.exceptions import InvalidPasswordException

from app.core.user import UserManager
from app.schemas import UserCreate


@pytest.mark.asyncio
async def test_password_too_short():

    manager = UserManager(user_db=object())

    with pytest.raises(InvalidPasswordException) as exc:
        await manager.validate_password(
            '12',
            UserCreate(email='test@test.com', password='12')
        )

    assert exc.value.reason == (
        'Пароль должен состоять как минимум из 3 символов.'
    )


@pytest.mark.asyncio
async def test_password_contains_email():

    manager = UserManager(user_db=object())

    with pytest.raises(InvalidPasswordException):
        await manager.validate_password(
            'test@test.com123',
            UserCreate(email='test@test.com', password='x')
        )


@pytest.mark.asyncio
async def test_password_ok():

    manager = UserManager(user_db=object())

    await manager.validate_password(
        'secure123',
        UserCreate(email='test@test.com', password='secure123')
    )
