from app.sessions.models import (
    Session
)

session = Session(
    session_id="session_001",
    user_id="dushyant"
)

print(session)