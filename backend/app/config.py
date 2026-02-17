from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENTRA_CLIENT_ID: str = ""
    ENTRA_CLIENT_SECRET: str = ""
    ENTRA_TENANT_ID: str = ""
    ENTRA_AUTHORITY: str = ""

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sso"

    JWT_SECRET: str = "change-me-to-a-random-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60

    FRONTEND_URL: str = "http://localhost:5173"

    model_config = {"env_file": ".env", "extra": "ignore"}

    @property
    def entra_authority(self) -> str:
        if self.ENTRA_AUTHORITY:
            return self.ENTRA_AUTHORITY
        return f"https://login.microsoftonline.com/{self.ENTRA_TENANT_ID}"


settings = Settings()
