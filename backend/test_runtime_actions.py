# test_runtime_actions.py

from app.runtime.runtime_loop import (
    RuntimeLoop
)

runtime = RuntimeLoop()

state = runtime.initialize(
    "AI Internship"
)

state = runtime.observe(
    state,
    "user123"
)

state = runtime.plan(
    state
)

state = runtime.act(
    state
)

print("\nTASK:\n")

print(
    state.current_task
)

print("\nRESULTS:\n")

print(
    state.action_results
)