from langchain_google_genai import ChatGoogleGenerativeAI
from jarvis.core.settings import llm_settings


llm = ChatGoogleGenerativeAI(
    model=llm_settings.MODEL_NAME,
    api_key=llm_settings.GOOGLE_API_KEY,
    temperature=llm_settings.TEMPERATURE,
    max_tokens=llm_settings.MAX_TOKENS,
    timeout=llm_settings.TIMEOUT,
    max_retries=llm_settings.MAX_RETRIES,
)
