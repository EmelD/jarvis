from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    VERSION: str = "0.0.0"


class LLMSettings(BaseSettings):
    MODEL_NAME: str = ""
    GOOGLE_API_KEY: str = ""
    TEMPERATURE: float = 1.0
    TIMEOUT: float = 40.0
    MAX_TOKENS: int = 1000
    MAX_RETRIES: int = 2


app_settings = ApplicationSettings()
llm_settings = LLMSettings()
