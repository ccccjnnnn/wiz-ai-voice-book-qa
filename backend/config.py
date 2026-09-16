"""Shared backend configuration for future application integration."""

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from dotenv import dotenv_values


ENV_PATH = Path(__file__).resolve().parent / ".env"


class ConfigurationError(RuntimeError):
    """A safe configuration error that never includes secret values."""


@dataclass(frozen=True)
class Settings:
    dashscope_api_key: str = field(repr=False)
    dashscope_base_url: str
    qwen_model: str
    deepgram_api_key: str = field(repr=False)


def load_voyage_api_key(path: Path = ENV_PATH) -> str:
    """Load the retrieval-only credential without changing frozen provider settings."""
    if not path.is_file():
        raise ConfigurationError("backend_env_missing")
    try:
        value = dotenv_values(path, interpolate=False).get("VOYAGE_API_KEY")
    except Exception:
        raise ConfigurationError("configuration_unreadable") from None
    if not value or not value.strip():
        raise ConfigurationError("voyage_api_key_missing")
    cleaned = value.strip()
    if any(character.isspace() for character in cleaned):
        raise ConfigurationError("voyage_api_key_invalid")
    return cleaned


def load_settings(path: Path = ENV_PATH) -> Settings:
    """Load backend/.env without interpolation or secret logging."""
    if not path.is_file():
        raise ConfigurationError("backend_env_missing")
    try:
        values = dotenv_values(path, interpolate=False)
        required = (
            "DASHSCOPE_API_KEY",
            "DASHSCOPE_BASE_URL",
            "QWEN_MODEL",
            "DEEPGRAM_API_KEY",
        )
        if any(not values.get(name) for name in required):
            raise ConfigurationError("required_configuration_missing")
        cleaned = {name: values[name].strip() for name in required}
    except ConfigurationError:
        raise
    except Exception:
        raise ConfigurationError("configuration_unreadable") from None

    if any(char.isspace() for char in cleaned["DASHSCOPE_API_KEY"]):
        raise ConfigurationError("dashscope_key_invalid")
    if any(char.isspace() for char in cleaned["DEEPGRAM_API_KEY"]):
        raise ConfigurationError("deepgram_key_invalid")

    return Settings(
        dashscope_api_key=cleaned["DASHSCOPE_API_KEY"],
        dashscope_base_url=cleaned["DASHSCOPE_BASE_URL"].rstrip("/"),
        qwen_model=cleaned["QWEN_MODEL"],
        deepgram_api_key=cleaned["DEEPGRAM_API_KEY"],
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()
