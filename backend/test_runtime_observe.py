from app.runtime.runtime_loop import (
    RuntimeLoop
)

runtime = RuntimeLoop()

state = runtime.run(

    goal="Get AI Internship",

    user_id="user123"
)

print()

print("PROFILE:")

print(
    state.profile_snapshot
)

print()

print("OBSERVATIONS:")

print(
    state.observations
)