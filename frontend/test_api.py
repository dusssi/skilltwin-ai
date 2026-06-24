from services.api import (
    get_profile
)

profile = (
    get_profile(
        "user123"
    )
)

print(profile)