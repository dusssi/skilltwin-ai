from app.sessions.models import (
    Session
)

from app.sessions.compressor import (
    ContextCompressor
)

session = Session(
    session_id="session_001",
    user_id="dushyant"
)

session.messages = [

    "I want AI Internship",

    "Teach Python",

    "Teach FastAPI",

    "Suggest Projects",

    "Help Resume",

    "Prepare Interviews"
]

compressor = ContextCompressor()

summary = compressor.compress(
    session
)

print(summary)