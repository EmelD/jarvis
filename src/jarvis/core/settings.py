from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    VERSION: str = "0.0.0"


app_settings = ApplicationSettings()
