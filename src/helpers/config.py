from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    BaseSettings is a ready-to-use class from pydantic_settings.
    → Its purpose is to handle environment variables automatically without using os.getenv() manually.
    
    When you define something like APP_NAME: str,
    → It means you're expecting the variable to be a string, 
      and if it’s not, it will raise a validation error automatically.

    SettingsConfigDict(env_file=".env")
    → This tells the class where to read the environment variables from (.env file).
      Even if the variables are not in the code, it still finds and loads them from the file.
    """

    # Define the environment variables and their types for validation
    APP_NAME: str
    APP_VERSION: str
    
    FILE_ALLOWED_TYPES: List[str]
    FILE_ALLOWED_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE:int

    MONGODB_URL : str
    MONGODB_DATBASE : str
    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None
    COHERE_API_KEY: str = None

    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None
    INPUT_DAFAULT_MAX_CHARACTERS: int = None
    GENERATION_DAFAULT_MAX_TOKENS: int = None
    GENERATION_DAFAULT_TEMPERATURE: float = None

    VECTOR_DB_BACKEND : str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_METHOD: str = None
    VECTOR_DB_BACKEND: str

    PRIMARY_LANG: str = "en"
    DEFAULT_LANG: str = "en"


    # Define model configuration and specify the .env file path
    model_config = SettingsConfigDict(env_file=".env")

# function return an object from setting class to use it later
def get_settings():
    return Settings()



