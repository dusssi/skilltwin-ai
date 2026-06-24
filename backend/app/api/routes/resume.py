from fastapi import APIRouter

from app.resume.analyzer import (
    ResumeAnalyzer
)

from app.api.schemas.requests import (
    ResumeRequest
)

from app.api.schemas.responses import (
    ResumeResponse
)

router = APIRouter()

analyzer = (
    ResumeAnalyzer()
)


@router.post(
    "/resume/analyze",
    response_model=ResumeResponse
)
def analyze_resume(
    request: ResumeRequest
):

    result = (
        analyzer.analyze(
            request.resume_text
        )
    )

    return ResumeResponse(

        extracted_skills=
        result.extracted_skills,

        missing_skills=
        result.missing_skills,

        recommended_projects=
        result.recommended_projects,

        readiness_score=
        result.readiness_score
    )