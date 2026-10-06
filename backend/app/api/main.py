"""SkillTwin API application factory (the single FastAPI app)."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors import register_error_handlers
from app.api.middleware import RateLimitMiddleware
from app.api.routes.auth import router as auth_router
from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.knowledge import router as knowledge_router
from app.api.routes.memory import router as memory_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.resume import router as resume_router
from app.api.routes.roadmap import router as roadmap_router
from app.api.routes.runtime import router as runtime_router
from app.api.routes.twin import router as twin_router
from app.config.settings import settings
from app.db.database import init_db
from app.twin.catalog import seed_catalog

logger = logging.getLogger("skilltwin")


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_TITLE, version=settings.APP_VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RateLimitMiddleware)
    register_error_handlers(app)

    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(twin_router)
    app.include_router(resume_router)
    app.include_router(chat_router)
    app.include_router(roadmap_router)
    app.include_router(runtime_router)
    app.include_router(memory_router)
    app.include_router(recommendations_router)
    app.include_router(knowledge_router)

    @app.get("/", tags=["health"])
    def home():
        return {"message": "SkillTwin API Running", "version": settings.APP_VERSION}

    @app.on_event("startup")
    def _startup() -> None:
        init_db()
        try:
            seed_catalog()
        except Exception as exc:  # pragma: no cover - startup safety
            logger.warning("Skill catalog seeding skipped: %s", exc)
        logger.info("SkillTwin API startup complete (db ready).")

    return app


app = create_app()
