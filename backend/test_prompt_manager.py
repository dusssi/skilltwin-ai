from app.llm.prompt_manager import (
    PromptManager
)

manager = PromptManager()

prompt = manager.build_prompt(

    query="How do I get an AI Internship?",

    context=(
        "Python required\n"
        "Git required\n"
        "Portfolio required"
    )
)

print(prompt)