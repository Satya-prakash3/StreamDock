from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str
    app_host: str
    app_port: int
    # mongo_uri: str
    # redis_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
