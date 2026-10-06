"""Personalized chat routes."""

from fastapi import APIRouter, Depends

from app.api.errors import bad_request, not_found
from app.api.schemas.requests import ChatRequest
from app.auth.dependencies import get_current_user
from app.chat.service import ChatService
from app.sessions.session_manager import SessionManager

router = APIRouter(tags=["chat"])

chat_service = ChatService()
sessions = SessionManager()


@router.post("/chat")
def chat(payload: ChatRequest, user: dict = Depends(get_current_user)):
    try:
        return chat_service.chat(user["id"], payload.message, payload.session_id)
    except ValueError as exc:
        raise bad_request(str(exc))


@router.get("/chat/sessions")
def list_chat_sessions(user: dict = Depends(get_current_user)):
    return {"sessions": sessions.list_sessions(user["id"])}


@router.get("/chat/sessions/{session_id}/messages")
def session_messages(session_id: str, user: dict = Depends(get_current_user)):
    session = sessions.get_session(user["id"], session_id)
    if not session:
        raise not_found("Session")
    return {"session": session, "messages": sessions.list_messages(user["id"], session_id)}
