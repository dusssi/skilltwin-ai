from app.runtime.runtime_loop import (
    RuntimeLoop
)

runtime = RuntimeLoop()

state = runtime.run(

    goal="AI Internship",

    user_id="user123"
)

print()

print("REFLECTION:")

print(
    state.reflection_results
)

print()

print("OBSERVATIONS:")

print(
    state.observations
)