from app.sessions.session_manager import (
    SessionManager
)

manager = SessionManager()

manager.create_session(
    "session_001",
    "dushyant"
)

manager.add_message(
    "session_001",
    "I want AI Internship"
)

manager.add_message(
    "session_001",
    "Create roadmap"
)

session = manager.get_session(
    "session_001"
)

print(session.messages)