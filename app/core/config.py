from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    description: str = 'Веб-сервис для бронирование переговорок'
    database_url: str
    secret: str
    first_superuser_email: Optional[EmailStr]
    first_superuser_password: Optional[str]

    class Config:
        env_file = '.env'


settings = Settings()
