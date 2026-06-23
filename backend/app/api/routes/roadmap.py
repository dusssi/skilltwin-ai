from fastapi import APIRouter

from app.profile.profile_manager import (
    ProfileManager
)

router = APIRouter()

profile_manager = (
    ProfileManager()
)


@router.get(
    "/roadmap/{user_id}"
)
def get_roadmap(
    user_id: str
):

    profile = (
        profile_manager.load_profile(
            user_id
        )
    )

    if not profile:

        return {

            "status": "error",

            "message":
            "Profile not found"
        }

    roadmap = []

    for skill in profile.missing_skills:

        roadmap.append(
            f"Learn {skill}"
        )

    roadmap.append(
        "Build Portfolio Projects"
    )

    roadmap.append(
        "Apply For AI Internships"
    )

    return {

        "status": "success",

        "user_id":
        profile.user_id,

        "goal":
        profile.primary_goal,

        "roadmap":
        roadmap
    }