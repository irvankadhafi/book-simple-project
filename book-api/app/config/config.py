from pydantic import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    class Config:
        env_file = ".env"


config = Config()
