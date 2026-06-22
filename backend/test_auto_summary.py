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
    "Teach Python"
)

manager.add_message(
    "session_001",
    "Teach FastAPI"
)

session = manager.get_session(
    "session_001"
)

print("Messages:\n")

print(
    session.messages
)

print("\nSummary:\n")

print(
    session.summary
)