from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./madhurplay.db"
    jwt_secret: str = "CHANGE_ME_IN_PRODUCTION"
    jwt_expire_minutes: int = 1440
    tmdb_api_read_access_token: str = ""
    frontend_origin: str = "http://localhost:5173"
    admin_email: str = "admin@example.com"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

settings = Settings()
