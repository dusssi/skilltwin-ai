from app.llm.provider import (
    LLMProvider
)

provider = LLMProvider()

response = provider.generate(

    "How do I get an AI Internship?"
)

print(response)