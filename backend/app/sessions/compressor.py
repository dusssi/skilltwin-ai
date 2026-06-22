from app.sessions.models import (
    Session
)


class ContextCompressor:

    def compress(
        self,
        session: Session
    ):

        if not session.messages:

            return ""

        summary = (
            " | ".join(
                session.messages[-5:]
            )
        )

        return summary