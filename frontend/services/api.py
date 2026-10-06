"""Typed SkillTwin backend client with structured error handling."""

import os

import requests

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
_TIMEOUT = 60


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


def _request(method: str, path: str, token: str | None = None, **kwargs) -> dict | list:
    headers = kwargs.pop("headers", {}) or {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.request(method, f"{BASE_URL}{path}", headers=headers,
                                    timeout=_TIMEOUT, **kwargs)
    except requests.ConnectionError:
        raise ApiError(0, "backend_unavailable",
                       f"Cannot reach the backend at {BASE_URL}. Is it running?")
    except requests.Timeout:
        raise ApiError(0, "timeout", "The backend took too long to respond.")
    if 200 <= response.status_code < 300:
        try:
            return response.json()
        except ValueError:
            return {}
    try:
        error = response.json().get("error", {})
        code = error.get("code", "http_error")
        message = error.get("message", f"Request failed ({response.status_code}).")
    except ValueError:
        code, message = "http_error", f"Request failed ({response.status_code})."
    raise ApiError(response.status_code, code, message)


def health() -> dict:
    return _request("GET", "/health")


# ------------------------------------------------------------------ auth
def register(username: str, password: str, display_name: str = "") -> dict:
    return _request("POST", "/auth/register",
                    json={"username": username, "password": password,
                          "display_name": display_name})


def login(username: str, password: str) -> dict:
    return _request("POST", "/auth/login", json={"username": username, "password": password})


def logout(token: str) -> dict:
    return _request("POST", "/auth/logout", token=token)


def me(token: str) -> dict:
    return _request("GET", "/auth/me", token=token)


# ------------------------------------------------------------------ twin
def get_twin(token: str) -> dict:
    return _request("GET", "/twin", token=token)


def update_twin(token: str, fields: dict) -> dict:
    return _request("PATCH", "/twin", token=token, json=fields)


def add_skill(token: str, name: str, level: int | None = None, note: str = "") -> dict:
    return _request("POST", "/twin/skills", token=token,
                    json={"name": name, "level": level, "note": note})


def get_gaps(token: str) -> dict:
    return _request("GET", "/twin/gaps", token=token)


def list_goals(token: str) -> dict:
    return _request("GET", "/twin/goals", token=token)


def create_goal(token: str, title: str, target_role: str = "") -> dict:
    return _request("POST", "/twin/goals", token=token,
                    json={"title": title, "target_role": target_role})


def list_projects(token: str) -> dict:
    return _request("GET", "/twin/projects", token=token)


def create_project(token: str, title: str, description: str = "",
                   skills: list | None = None, status: str = "planned") -> dict:
    return _request("POST", "/twin/projects", token=token,
                    json={"title": title, "description": description,
                          "skills": skills or [], "status": status})


# ---------------------------------------------------------------- resume
def analyze_resume_text(token: str, resume_text: str) -> dict:
    return _request("POST", "/resume/analyze", token=token, json={"resume_text": resume_text})


def upload_resume(token: str, uploaded_file) -> dict:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
    return _request("POST", "/resume/upload", token=token, files=files)


def resume_history(token: str) -> dict:
    return _request("GET", "/resume/history", token=token)


# ------------------------------------------------------------------ chat
def chat(token: str, message: str, session_id: str | None = None) -> dict:
    return _request("POST", "/chat", token=token,
                    json={"message": message, "session_id": session_id})


def chat_sessions(token: str) -> dict:
    return _request("GET", "/chat/sessions", token=token)


def session_messages(token: str, session_id: str) -> dict:
    return _request("GET", f"/chat/sessions/{session_id}/messages", token=token)


# ---------------------------------------------------------------- roadmap
def get_roadmap(token: str) -> dict:
    return _request("GET", "/roadmap", token=token)


def generate_roadmap(token: str, goal: str | None = None) -> dict:
    return _request("POST", "/roadmap/generate", token=token, json={"goal": goal})


def update_roadmap_item(token: str, item_id: int, status: str) -> dict:
    return _request("PATCH", f"/roadmap/items/{item_id}", token=token,
                    json={"status": status})


# ---------------------------------------------------------------- runtime
def run_runtime(token: str, goal: str | None = None) -> dict:
    return _request("POST", "/runtime", token=token, json={"goal": goal})


# ---------------------------------------------------------------- memory
def list_memory(token: str, query: str | None = None) -> dict:
    params = {"q": query} if query else {}
    return _request("GET", "/memory", token=token, params=params)


def list_events(token: str) -> dict:
    return _request("GET", "/memory/events", token=token)


# -------------------------------------------------------- recommendations
def list_recommendations(token: str) -> dict:
    return _request("GET", "/recommendations", token=token)


def generate_recommendations(token: str) -> dict:
    return _request("POST", "/recommendations/generate", token=token)


def update_recommendation(token: str, rec_id: int, status: str) -> dict:
    return _request("PATCH", f"/recommendations/{rec_id}", token=token,
                    json={"status": status})
