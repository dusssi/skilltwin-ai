import json
import os

from app.profile.models import (
    UserProfile
)


class ProfileManager:

    PROFILE_DIR = (
        "data/profiles"
    )

    def __init__(self):

        os.makedirs(
            self.PROFILE_DIR,
            exist_ok=True
        )

    def create_profile(
        self,
        user_id: str
    ):

        profile = UserProfile(
            user_id=user_id
        )

        self.save_profile(
            profile
        )

        return profile

    def save_profile(
        self,
        profile: UserProfile
    ):

        filepath = (

            f"{self.PROFILE_DIR}/"
            f"{profile.user_id}.json"
        )

        with open(
            filepath,
            "w"
        ) as file:

            json.dump(

                profile.model_dump(),

                file,

                indent=4
            )

    def load_profile(
        self,
        user_id: str
    ):

        filepath = (

            f"{self.PROFILE_DIR}/"
            f"{user_id}.json"
        )

        if not os.path.exists(
            filepath
        ):

            return None

        with open(
            filepath,
            "r"
        ) as file:

            data = json.load(
                file
            )

        return UserProfile(
            **data
        )

    def get_profile(
        self,
        user_id: str
    ):

        return self.load_profile(
            user_id
        )