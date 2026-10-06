"""Health and readiness endpoints (no auth required)."""

from fastapi import APIRouter

from app.config.settings import settings
from app.db.database import check_ready

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {
        "status": "ok",
        "version": settings.APP_VERSION,
        "database_ready": check_ready(),
        "llm_configured": settings.llm_configured,
    }


@router.get("/ready")
def ready():
    from fastapi.responses import JSONResponse

    if not check_ready():
        return JSONResponse(status_code=503, content={"ready": False})
    return {"ready": True}
