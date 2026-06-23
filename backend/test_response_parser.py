from app.llm.response_parser import (
    ResponseParser
)

parser = ResponseParser()

response = parser.parse(

    content=(
        "Learn Python, Git, "
        "and build projects."
    ),

    provider="Gemini",

    model="gemini-2.5-flash"
)

print(response)