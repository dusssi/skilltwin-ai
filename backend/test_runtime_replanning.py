from app.runtime.runtime_loop import (
    RuntimeLoop
)

runtime = RuntimeLoop()

state = runtime.run(

    goal="AI Internship",

    user_id="user123"
)

print()

print("FINAL SCORE:")
print(state.reflection_results)

print()

print("ITERATIONS:")
print(state.iteration_count)

print()

print("FINAL PLAN:")
print(state.plan)

print()

print("OBSERVATIONS:")
print(state.observations)