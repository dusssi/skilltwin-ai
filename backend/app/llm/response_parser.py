from app.llm.models import (
    LLMResponse
)


class ResponseParser:

    def parse(
        self,
        content: str,
        provider: str,
        model: str
    ):

        return LLMResponse(

            content=content,

            provider=provider,

            model=model
        )