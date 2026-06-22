from app.sessions.models import (
    Session
)

from app.sessions.compressor import (
    ContextCompressor
)


class SessionManager:

    def __init__(self):

        self.sessions = {}

        self.compressor = (
            ContextCompressor()
        )

    def create_session(
        self,
        session_id: str,
        user_id: str
    ):

        session = Session(
            session_id=session_id,
            user_id=user_id
        )

        self.sessions[
            session_id
        ] = session

        return session

    def get_session(
        self,
        session_id: str
    ):

        return self.sessions.get(
            session_id
        )

    def add_message(
        self,
        session_id: str,
        message: str
    ):

        session = self.get_session(
            session_id
        )

        if session:

            session.messages.append(
                message
            )

            session.summary = (
                self.compressor.compress(
                    session
                )
            )

            return True

        return False