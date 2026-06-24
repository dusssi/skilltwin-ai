import requests

BASE_URL = (
    "http://127.0.0.1:8000"
)


def get_profile(
    user_id: str
):

    response = requests.get(
        f"{BASE_URL}/profile/{user_id}"
    )

    return response.json()


def get_roadmap(
    user_id: str
):

    response = requests.get(
        f"{BASE_URL}/roadmap/{user_id}"
    )

    return response.json()


def chat(
    user_id: str,
    message: str
):

    response = requests.post(

        f"{BASE_URL}/chat",

        json={

            "user_id":
            user_id,

            "message":
            message
        }
    )

    return response.json()


def run_runtime(
    user_id: str,
    goal: str
):

    response = requests.post(

        f"{BASE_URL}/runtime",

        json={

            "user_id":
            user_id,

            "goal":
            goal
        }
    )

    return response.json()