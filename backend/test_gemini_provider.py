from app.llm.provider import (
    LLMProvider
)

provider = LLMProvider()

response = provider.generate(

    """
    Explain AI internships in 3 lines.
    """
)

print()

print("CONTENT:\n")

print(response.content)

print()

print("PROVIDER:")

print(response.provider)

print()

print("MODEL:")

print(response.model)