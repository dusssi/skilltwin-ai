"""Unit tests for validated LLM output parsing."""

import pytest
from pydantic import BaseModel

from app.llm.response_parser import ResponseParser


class _Item(BaseModel):
    title: str
    count: int


def test_parse_rejects_empty():
    with pytest.raises(ValueError):
        ResponseParser().parse("  ", "Gemini", "m")


def test_parse_json_plain_object():
    item = ResponseParser().parse_json('{"title": "A", "count": 3}', _Item)
    assert (item.title, item.count) == ("A", 3)


def test_parse_json_code_fence():
    item = ResponseParser().parse_json('```json\n{"title": "B", "count": 1}\n```', _Item)
    assert item.title == "B"


def test_parse_json_rejects_invalid_json():
    with pytest.raises(ValueError):
        ResponseParser().parse_json("not json at all", _Item)


def test_parse_json_rejects_schema_violation():
    with pytest.raises(ValueError):
        ResponseParser().parse_json('{"title": "C"}', _Item)
