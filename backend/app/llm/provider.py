import google.generativeai as genai

from app.llm.models import (
    LLMResponse
)

from app.config.settings import (
    settings
)


class LLMProvider:

    def __init__(self):

        genai.configure(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = (
            genai.GenerativeModel(
                "gemini-2.5-flash"
            )
        )

    def generate(
        self,
        prompt: str
    ) -> LLMResponse:

        try:

            response = (
                self.model.generate_content(
                    prompt
                )
            )

            return LLMResponse(

                content=response.text,

                provider="Gemini",

                model="gemini-2.5-flash"
            )

        except Exception as e:

            error_message = str(e)

            # Gemini quota/rate limit fallback

            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
                or "quota" in error_message.lower()
            ):

                return LLMResponse(

                    content=(
                        "Gemini quota exceeded.\n\n"
                        "SkillTwin Fallback Advice:\n"
                        "1. Learn Python\n"
                        "2. Learn Git & GitHub\n"
                        "3. Build Projects\n"
                        "4. Create a Portfolio\n"
                        "5. Apply Consistently"
                    ),

                    provider="Fallback",

                    model="Template"
                )

            # Generic fallback

            return LLMResponse(

                content=(
                    f"SkillTwin encountered an error.\n\n"
                    f"Details: {error_message}"
                ),

                provider="Fallback",

                model="ErrorHandler"
            )