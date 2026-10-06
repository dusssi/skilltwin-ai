"""Resume agent: runs the resume → Twin pipeline for text input."""

from app.resume.service import ResumeService


class ResumeAgent:
    name = "resume_agent"

    def __init__(self):
        self.service = ResumeService()

    def run(self, user_id: str, resume_text: str) -> dict:
        return self.service.analyze_text(user_id, resume_text)
