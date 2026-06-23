from app.profile.profile_manager import (
    ProfileManager
)

manager = ProfileManager()

profile = manager.create_profile(
    "user123"
)

profile.primary_goal = (
    "AI Internship"
)

profile.skills = [
    "Python",
    "FastAPI"
]

manager.save_profile(
    profile
)

loaded_profile = (
    manager.load_profile(
        "user123"
    )
)

print()

print("LOADED PROFILE:\n")

print(
    loaded_profile
)