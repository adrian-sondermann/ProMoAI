from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
_DOTENV_FILE: Path = _PROJECT_ROOT / ".env"

# Force reload and override existing environment variables from .env file
load_dotenv(dotenv_path=_DOTENV_FILE, override=True)


class _AzureOpenAI(BaseSettings):
    """
    Configuration for Azure OpenAI Endpoints.
    Reads environment variables from `.env` file (case-insensitive) with prefix `AZURE_OPENAI_`.
    """

    base_url: str = ""  # set in .env file to use Azure OpenAI Endpoints
    model_name: str = "gpt-4o"
    model_version: str = "2024-05-13"
    api_key: str = ""  # set in .env file to use Azure OpenAI Endpoints

    model_config = SettingsConfigDict(
        env_file=_DOTENV_FILE, env_prefix="AZURE_OPENAI_", extra="ignore"
    )


class _PortalAPI(BaseSettings):
    """
    Configuration for the LangChain AI Portal API.
    Reads environment variables from `.env` file (case-insensitive) with prefix `PORTAL_API_`.
    """

    host: str = ""  # set in .env file to use the Langchain AI Portal API
    port: int = 443
    sdk_api_key: str = ""  # set in .env file to use the Langchain AI Portal API
    use_ssl: bool = True

    model_config = SettingsConfigDict(
        env_file=_DOTENV_FILE, env_prefix="PORTAL_API_", extra="ignore"
    )


class _LOGGING(BaseSettings):
    """
    Configuration for logging.
    Reads environment variables from `.env` file (case-insensitive) with prefix `LOGGING_`.
    """

    enable_prints: bool = False

    model_config = SettingsConfigDict(
        env_file=_DOTENV_FILE, env_prefix="LOGGING_", extra="ignore"
    )


class Config(BaseSettings):
    """
    Configuration for ProMoAI.
    Reads environment variables from `.env` file (case-insensitive).

    Attributes:
        azure_openai (_AzureOpenAI): Configuration for Azure OpenAI endpoints.
        portal_api (_PortalAPI): Configuration for the LangChain AI Portal API.
        logging (_LOGGING): Configuration for logging.
    """

    azure_openai: _AzureOpenAI = _AzureOpenAI()
    "Configuration for Azure OpenAI Endpoints"
    portal_api: _PortalAPI = _PortalAPI()
    "Configuration for the LangChain AI Portal API."

    logging: _LOGGING = _LOGGING()
    "Configuration for logging"

    model_config = SettingsConfigDict(
        env_file=_DOTENV_FILE, env_prefix="", extra="allow"
    )


config = Config()
