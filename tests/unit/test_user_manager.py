import types

import pytest

from fastapi_users.authentication import JWTStrategy
from fastapi_users.exceptions import InvalidPasswordException

from app.core.config import settings
from app.core.user import UserManager, auth_backend, get_jwt_strategy


@pytest.fixture
def manager() -> UserManager:
    return UserManager(user_db=object())


@pytest.fixture
def user():
    return types.SimpleNamespace(email='test@test.com')


@pytest.mark.asyncio
async def test_validate_password_too_short(manager, user):
    with pytest.raises(InvalidPasswordException) as exc_info:
        await manager.validate_password('12', user)

    assert exc_info.value.reason == (
        'Пароль должен состоять как минимум из 3 символов.'
    )


@pytest.mark.asyncio
async def test_validate_password_contains_email(manager, user):
    with pytest.raises(InvalidPasswordException) as exc_info:
        await manager.validate_password('test@test.com!!', user)

    assert exc_info.value.reason == (
        'Пароль не должен содержать адрес электронной почты.'
    )


@pytest.mark.asyncio
async def test_validate_password_valid(manager):
    other_user = types.SimpleNamespace(email='other@example.com')

    result = await manager.validate_password('secure123', other_user)

    assert result is None


def test_get_jwt_strategy_config():
    strategy = get_jwt_strategy()

    assert isinstance(strategy, JWTStrategy)
    assert strategy.lifetime_seconds == 3600
    assert strategy.secret == settings.secret


def test_auth_backend_name():
    assert auth_backend.name == 'jwt'


@pytest.mark.asyncio
async def test_on_after_register_smoke(manager, user, capsys):
    result = await manager.on_after_register(user)

    assert result is None

    captured = capsys.readouterr()
    assert 'test@test.com' in captured.out
