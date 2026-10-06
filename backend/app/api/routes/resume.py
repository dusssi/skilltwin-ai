"""Resume routes: text analysis, secure PDF upload, history."""

import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile

from app.api.errors import bad_request, payload_too_large
from app.api.schemas.requests import ResumeTextRequest
from app.auth.dependencies import get_current_user
from app.config.settings import settings
from app.db import content as content_repo
from app.resume.service import ResumeService

router = APIRouter(prefix="/resume", tags=["resume"])

service = ResumeService()


def _safe_pdf_filename(original: str) -> str:
    suffix = Path(original or "").suffix.lower()
    if suffix not in settings.ALLOWED_UPLOAD_EXTENSIONS:
        raise bad_request("Only PDF files are accepted.")
    return f"{uuid.uuid4().hex}.pdf"


@router.post("/analyze", status_code=201)
def analyze_text(payload: ResumeTextRequest, user: dict = Depends(get_current_user)):
    return service.analyze_text(user["id"], payload.resume_text)


@router.post("/upload", status_code=201)
async def upload_resume(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
):
    original = file.filename or "resume.pdf"
    stored_name = _safe_pdf_filename(original)

    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    content = await file.read(max_bytes + 1)
    if len(content) > max_bytes:
        raise payload_too_large(f"File exceeds the {settings.MAX_UPLOAD_MB} MB limit.")
    if len(content) < 20 or not content[:5] == b"%PDF-":
        raise bad_request("Uploaded file is not a valid PDF.")

    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    destination = upload_dir / stored_name
    # Defense in depth: resolve and confirm containment (no traversal).
    if upload_dir.resolve() not in destination.resolve().parents:
        raise bad_request("Invalid upload path.")
    destination.write_bytes(content)

    return service.analyze_pdf(
        user_id=user["id"],
        file_path=str(destination),
        filename_original=Path(original).name[:200],
        filename_stored=stored_name,
    )


@router.get("/history")
def resume_history(user: dict = Depends(get_current_user)):
    return {
        "resumes": content_repo.list_resumes(user["id"]),
        "analyses": content_repo.list_resume_analyses(user["id"]),
    }
