from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60
    cosmos_db_uri: str
    cosmos_db_key: str
    cosmos_db_database: str
    TELEGRAM_BOT_TOKEN: str
    thread_inactivity_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()
