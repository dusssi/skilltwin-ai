from app.llm.models import (
    LLMResponse
)

response = LLMResponse(

    content="Hello",

    provider="Gemini",

    model="gemini-2.5-flash"
)

print(response)