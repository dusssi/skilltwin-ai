"""Shared pytest fixtures: isolated temp DB + uploads + TestClient."""

import os

import pytest
from fastapi.testclient import TestClient

from app.api.middleware import reset_rate_limit
from app.config.settings import settings
from app.db.database import init_db
from app.twin.catalog import seed_catalog


@pytest.fixture()
def tmp_env(tmp_path, monkeypatch):
    """Point the app at a fresh temp database and upload dir."""
    db_path = tmp_path / "test.db"
    upload_dir = tmp_path / "uploads"
    monkeypatch.setattr(settings, "DATABASE_PATH", str(db_path))
    monkeypatch.setattr(settings, "UPLOAD_DIR", str(upload_dir))
    monkeypatch.setattr(settings, "RATE_LIMIT_ENABLED", False)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    init_db()
    seed_catalog()
    reset_rate_limit()
    return {"db": str(db_path), "uploads": str(upload_dir)}


@pytest.fixture()
def client(tmp_env):
    from app.api.main import create_app

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


def register(client: TestClient, username: str = "alice", password: str = "password123",
             display_name: str = "Alice") -> dict:
    response = client.post("/auth/register", json={
        "username": username, "password": password, "display_name": display_name,
    })
    assert response.status_code == 201, response.text
    return response.json()


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def alice(client):
    data = register(client, "alice")
    return {"token": data["token"], "user": data["user"],
            "headers": auth_headers(data["token"])}


@pytest.fixture()
def bob(client):
    data = register(client, "bob", display_name="Bob")
    return {"token": data["token"], "user": data["user"],
            "headers": auth_headers(data["token"])}


class StubProvider:
    """Deterministic stand-in for the LLM provider (no network)."""

    def __init__(self, text="STUB RESPONSE", echo_prompt=False):
        self.text = text
        self.echo_prompt = echo_prompt
        self.configured = True
        self.calls: list = []

    def generate(self, prompt, system=None, temperature=None, max_output_tokens=None):
        from app.llm.models import LLMResponse

        self.calls.append({"prompt": prompt, "system": system})
        content = f"ECHO:{prompt[:2000]}" if self.echo_prompt else self.text
        return LLMResponse(content=content, provider="Stub", model="stub", fallback=False)


def minimal_pdf_bytes(lines: list) -> bytes:
    """Build a minimal valid single-page PDF containing the given text lines."""
    text_ops = "".join(
        f"BT /F1 12 Tf 50 {750 - i * 20} Td ({line}) Tj ET\n" for i, line in enumerate(lines)
    )
    stream = text_ops.encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"endstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"
    xref_at = len(pdf)
    pdf += f"xref\n0 {len(objects) + 1}\n".encode()
    pdf += b"0000000000 65535 f \n"
    for offset in offsets:
        pdf += f"{offset:010d} 00000 n \n".encode()
    pdf += (f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_at}\n%%EOF").encode()
    return bytes(pdf)
