from app.rag.prompt_builder import (
    PromptBuilder
)

builder = PromptBuilder()

prompt = builder.build(

    query="How do I get an AI Internship?",

    context=(
        "Python required\n"
        "Git required\n"
        "Portfolio required"
    )
)

print(prompt)