"""Gemini LLM provider over plain HTTPS (no heavy SDK needed).

* Model, timeout, retries and temperature come from environment settings.
* Transient failures (429/5xx, timeouts) are retried with backoff.
* Users never see raw exceptions or API internals.
* When no API key is configured, :class:`LLMUnavailableError` is raised so
  callers can use the honest, Twin-derived local composer instead.
"""

import logging
import time

import httpx

from app.config.settings import settings
from app.llm.models import LLMResponse

logger = logging.getLogger("skilltwin.llm")


class LLMError(Exception):
    """Base class for LLM failures (safe messages only)."""


class LLMUnavailableError(LLMError):
    """Raised when the LLM is not configured or unreachable."""


class LLMProvider:
    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout: int | None = None,
        max_retries: int | None = None,
    ):
        self.api_key = api_key if api_key is not None else settings.GEMINI_API_KEY
        self.model = model or settings.GEMINI_MODEL
        self.timeout = timeout or settings.LLM_TIMEOUT_SECONDS
        self.max_retries = max_retries if max_retries is not None else settings.LLM_MAX_RETRIES

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
    ) -> LLMResponse:
        if not self.configured:
            raise LLMUnavailableError("LLM is not configured.")
        if not prompt or not prompt.strip():
            raise LLMError("Empty prompt.")
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": settings.LLM_TEMPERATURE if temperature is None else temperature,
                "maxOutputTokens": (
                    settings.LLM_MAX_OUTPUT_TOKENS
                    if max_output_tokens is None
                    else max_output_tokens
                ),
            },
        }
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}

        url = (
            f"{settings.GEMINI_API_BASE}/v1beta/models/{self.model}:generateContent"
        )
        last_error = "unknown error"
        attempts = max(1, self.max_retries + 1)
        for attempt in range(attempts):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(url, params={"key": self.api_key}, json=payload)
                if response.status_code == 200:
                    text = self._extract_text(response.json())
                    if not text:
                        raise LLMError("The model returned an empty response.")
                    return LLMResponse(
                        content=text, provider="Gemini", model=self.model, fallback=False
                    )
                last_error = f"HTTP {response.status_code}"
                logger.warning("Gemini request failed: HTTP %s", response.status_code)
                if response.status_code not in {429, 500, 502, 503, 504}:
                    break
            except httpx.TimeoutException:
                last_error = "timeout"
                logger.warning("Gemini request timed out (attempt %d)", attempt + 1)
            except httpx.HTTPError as exc:
                last_error = exc.__class__.__name__
                logger.warning("Gemini transport error: %s", last_error)
            if attempt < attempts - 1:
                time.sleep(min(8, 2 ** attempt))
        raise LLMUnavailableError(
            "The AI service is temporarily unavailable. Please try again shortly."
        )

    @staticmethod
    def _extract_text(data: dict) -> str:
        try:
            candidates = data.get("candidates", [])
            if not candidates:
                return ""
            parts = candidates[0].get("content", {}).get("parts", [])
            return "".join(part.get("text", "") for part in parts).strip()
        except (AttributeError, TypeError, IndexError, KeyError):
            return ""
