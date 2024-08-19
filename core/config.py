import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

RS_KEY_PATH = BASE_DIR / "core" / "certs"

APP_ENV = os.getenv("APP_ENV", "development")


class DBSettings(BaseSettings):
    app_env: str = "development"

    db_name: str
    db_host: str
    db_port: int
    db_user: str
    db_pass: str

    sql_db_name: str

    @property
    def db_url(self) -> str:
        if (APP_ENV == "production"):
            return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
        else:
            return f"sqlite+aiosqlite:///{str(BASE_DIR/self.sql_db_name)}.sqlite"

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class JWTSettings(BaseSettings):
    algorithm: str = "RS256"
    private_key_path: Path = RS_KEY_PATH / "jwt-private.pem"
    public_key_path: Path = RS_KEY_PATH / "jwt-public.pem"
    access_token_expires_minutes: int = 30
    refresh_token_expires_minutes: int = 60

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class Settings(DBSettings):
    app_env: str = APP_ENV

    debug: bool = True

    db: DBSettings = DBSettings()

    jwt: JWTSettings = JWTSettings()

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()