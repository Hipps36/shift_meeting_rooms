from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    description: str = 'Веб-сервис для бронирование переговорок'
    database_url: str
    secret: str

    class Config:
        env_file = '.env'


settings = Settings()
