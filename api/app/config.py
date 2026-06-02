from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 15

    class Config:
        env_file = ".env"

settings = Settings()
