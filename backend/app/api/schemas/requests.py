from pydantic import BaseModel


class ChatRequest(
    BaseModel
):

    user_id: str

    message: str


class RuntimeRequest(
    BaseModel
):

    user_id: str

    goal: str


class ProfileRequest(
    BaseModel
):

    user_id: str


class ResumeRequest(
    BaseModel
):

    resume_text: str