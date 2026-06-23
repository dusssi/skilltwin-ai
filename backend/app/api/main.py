from fastapi import FastAPI

from app.api.routes.runtime import (
    router as runtime_router
)

from app.api.routes.profile import (
    router as profile_router
)

from app.api.routes.chat import (
    router as chat_router
)

from app.api.routes.roadmap import (
    router as roadmap_router
)

app = FastAPI(

    title="SkillTwin API",

    version="1.0.0"
)

app.include_router(
    runtime_router
)

app.include_router(
    profile_router
)

app.include_router(
    chat_router
)

app.include_router(
    roadmap_router
)


@app.get("/")
def home():

    return {

        "message":
        "SkillTwin API Running"
    }