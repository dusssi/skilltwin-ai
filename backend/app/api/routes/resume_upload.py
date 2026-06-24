from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import os

from app.resume.service import (
    ResumeService
)

from app.api.schemas.responses import (
    ResumeResponse
)

router = APIRouter()

resume_service = (
    ResumeService()
)


@router.post(
    "/resume/upload",
    response_model=ResumeResponse
)
async def upload_resume(
    file: UploadFile = File(...)
):

    uploads_dir = "uploads"

    os.makedirs(
        uploads_dir,
        exist_ok=True
    )

    file_path = os.path.join(

        uploads_dir,

        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        content = await file.read()

        buffer.write(
            content
        )

    result = (
        resume_service.analyze_pdf(
            file_path
        )
    )

    return ResumeResponse(

        extracted_skills=
        result.extracted_skills,

        missing_skills=
        result.missing_skills,

        recommended_projects=
        result.recommended_projects,

        recommended_internships=
        result.recommended_internships,

        readiness_score=
        result.readiness_score
    )