from fastapi import APIRouter

from app.profile.profile_manager import (
    ProfileManager
)

router = APIRouter()

profile_manager = (
    ProfileManager()
)


@router.get(
    "/profile/{user_id}"
)
def get_profile(
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

    return {

        "status": "success",

        "profile":
        profile.model_dump()
    }