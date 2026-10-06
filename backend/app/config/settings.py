"""Central application settings.

All configuration comes from environment variables (optionally via a
``.env`` file at the repository root or backend directory). No secrets are
hardcoded anywhere in the codebase.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_ROOT.parent

# Load .env from backend/ first, then repo root (first found wins per key).
load_dotenv(BACKEND_ROOT / ".env")
load_dotenv(REPO_ROOT / ".env")


def _getenv(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def _getenv_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def _getenv_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        return default


def _getenv_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    """Mutable settings object.

    Attributes are read at call time (not import time) so tests can
    monkeypatch values such as ``DATABASE_PATH`` safely.
    """

    # ---- LLM ----
    GEMINI_API_KEY: str = _getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = _getenv("GEMINI_MODEL", "gemini-2.5-flash")
    GEMINI_API_BASE: str = _getenv(
        "GEMINI_API_BASE", "https://generativelanguage.googleapis.com"
    )
    LLM_TIMEOUT_SECONDS: int = _getenv_int("LLM_TIMEOUT_SECONDS", 30)
    LLM_MAX_RETRIES: int = _getenv_int("LLM_MAX_RETRIES", 2)
    LLM_TEMPERATURE: float = _getenv_float("LLM_TEMPERATURE", 0.2)
    LLM_MAX_OUTPUT_TOKENS: int = _getenv_int("LLM_MAX_OUTPUT_TOKENS", 1024)

    # ---- Database ----
    DATABASE_PATH: str = _getenv(
        "SKILLTWIN_DB_PATH", str(BACKEND_ROOT / "data" / "skilltwin.db")
    )

    # ---- Uploads ----
    UPLOAD_DIR: str = _getenv("SKILLTWIN_UPLOAD_DIR", str(BACKEND_ROOT / "uploads"))
    MAX_UPLOAD_MB: int = _getenv_int("SKILLTWIN_MAX_UPLOAD_MB", 5)
    ALLOWED_UPLOAD_EXTENSIONS: tuple = (".pdf",)

    # ---- Auth ----
    TOKEN_EXPIRE_HOURS: int = _getenv_int("SKILLTWIN_TOKEN_EXPIRE_HOURS", 72)
    PASSWORD_MIN_LENGTH: int = _getenv_int("SKILLTWIN_PASSWORD_MIN_LENGTH", 8)

    # ---- API security ----
    CORS_ORIGINS: list = [
        origin.strip()
        for origin in _getenv(
            "SKILLTWIN_CORS_ORIGINS",
            "http://localhost:8501,http://127.0.0.1:8501",
        ).split(",")
        if origin.strip()
    ]
    RATE_LIMIT_ENABLED: bool = _getenv_bool("SKILLTWIN_RATE_LIMIT_ENABLED", True)
    RATE_LIMIT_PER_MINUTE: int = _getenv_int("SKILLTWIN_RATE_LIMIT_PER_MINUTE", 120)
    RATE_LIMIT_SENSITIVE_PER_MINUTE: int = _getenv_int(
        "SKILLTWIN_RATE_LIMIT_SENSITIVE_PER_MINUTE", 15
    )

    # ---- RAG ----
    RAG_SIMILARITY_THRESHOLD: float = _getenv_float(
        "SKILLTWIN_RAG_THRESHOLD", 0.12
    )
    RAG_TOP_K: int = _getenv_int("SKILLTWIN_RAG_TOP_K", 3)

    # ---- App ----
    APP_TITLE: str = "SkillTwin API"
    APP_VERSION: str = "2.0.0"
    LOG_LEVEL: str = _getenv("SKILLTWIN_LOG_LEVEL", "info")

    @property
    def llm_configured(self) -> bool:
        return bool(self.GEMINI_API_KEY)


settings = Settings()
