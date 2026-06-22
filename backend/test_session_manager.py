from app.sessions.session_manager import (
    SessionManager
)

manager = SessionManager()

session = manager.create_session(
    "session_001",
    "dushyant"
)

print(session)

loaded = manager.get_session(
    "session_001"
)

print("\nLoaded Session:\n")

print(loaded)