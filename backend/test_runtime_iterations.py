# test_runtime_iterations.py

from app.runtime.runtime_loop import (
    RuntimeLoop
)

runtime = RuntimeLoop()

state = runtime.run(
    "Get AI Internship"
)

print()

print("STATUS:")
print(state.status)

print()

print("ITERATIONS:")
print(state.iteration_count)

print()

print("CURRENT TASK:")
print(state.current_task)

print()

print("COMPLETED TASKS:")
print(state.completed_tasks)

print()

print("ACTIONS:")
print(state.actions_taken)

print()

print("OBSERVATIONS:")
print(state.observations)