# test_dynamic_planning.py

from app.runtime.runtime_loop import (
    RuntimeLoop
)

runtime = RuntimeLoop()

state = runtime.initialize(
    "Get AI Internship"
)

state = runtime.observe(
    state,
    "user123"
)

state = runtime.plan(
    state
)

print("\nPLAN:\n")

for task in state.plan:

    print(task)