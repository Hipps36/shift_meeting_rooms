from app.core.config import Settings, settings


def test_database_url_uses_asyncpg_driver():
    assert settings.database_url.startswith('postgresql+asyncpg')


def test_secret_is_non_empty_string():
    assert isinstance(settings.secret, str)
    assert settings.secret != ''


def test_app_title_and_description_are_non_empty():
    assert isinstance(settings.app_title, str)
    assert settings.app_title != ''
    assert isinstance(settings.description, str)
    assert settings.description != ''


def test_settings_honor_explicit_values_and_defaults():
    custom = Settings(
        database_url='postgresql+asyncpg://u:p@h/db',
        secret='s',
        _env_file=None,
    )
    assert custom.database_url == 'postgresql+asyncpg://u:p@h/db'
    assert custom.secret == 's'
    assert custom.first_superuser_email is None
