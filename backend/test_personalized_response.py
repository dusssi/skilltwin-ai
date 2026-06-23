from app.profile.profile_manager import (
    ProfileManager
)

from app.profile.response_engine import (
    PersonalizedResponseEngine
)

manager = ProfileManager()

profile = (
    manager.load_profile(
        "user123"
    )
)

engine = (
    PersonalizedResponseEngine()
)

response = (
    engine.generate(
        profile
    )
)

print()

print(response)