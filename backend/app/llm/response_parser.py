"""Validated parsing of LLM output (plain text + structured JSON)."""

import json
import re

from pydantic import BaseModel, ValidationError

from app.llm.models import LLMResponse


class ResponseParser:
    def parse(self, content: str, provider: str, model: str) -> LLMResponse:
        text = (content or "").strip()
        if not text:
            raise ValueError("Empty LLM content.")
        return LLMResponse(content=text, provider=provider, model=model, fallback=False)

    def parse_json(self, content: str, schema: type[BaseModel]) -> BaseModel:
        """Extract a JSON object from model text and validate it strictly."""
        text = (content or "").strip()
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
        candidate = match.group(1) if match else text
        if not match:
            start, end = candidate.find("{"), candidate.rfind("}")
            if start != -1 and end != -1 and end > start:
                candidate = candidate[start:end + 1]
        try:
            data = json.loads(candidate)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Model did not return valid JSON: {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError("Model JSON must be an object.")
        try:
            return schema.model_validate(data)
        except ValidationError as exc:
            raise ValueError(f"Model JSON failed validation: {exc}") from exc
