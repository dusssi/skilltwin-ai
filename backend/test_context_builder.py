from app.rag.context_builder import (
    ContextBuilder
)

builder = ContextBuilder()

context = builder.build(

    [
        "Python required",
        "Git required",
        "Portfolio required"
    ]
)

print(context)