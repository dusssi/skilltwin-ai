from pydantic import BaseModel

from typing import Dict
from typing import Any


class ChatResponse(
    BaseModel
):

    response: str


class RuntimeResponse(
    BaseModel
):

    status: str

    result: Dict[
        str,
        Any
    ]


class ProfileResponse(
    BaseModel
):

    profile: Dict[
        str,
        Any
    ]