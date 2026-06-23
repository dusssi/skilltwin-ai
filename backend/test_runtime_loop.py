from app.runtime.runtime_loop import (
    RuntimeLoop
)

runtime = RuntimeLoop()

state = runtime.initialize(
    "Get AI Internship"
)

state = runtime.observe(
    state
)

state = runtime.plan(
    state
)

state = runtime.act(
    state
)

state = runtime.reflect(
    state
)

state = runtime.finish(
    state
)

print()

print(state)