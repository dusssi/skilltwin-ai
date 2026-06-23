from app.runtime.runtime_models import (
    RuntimeState
)

from app.profile.profile_manager import (
    ProfileManager
)


class RuntimeLoop:

    def __init__(self):

        self.profile_manager = (
            ProfileManager()
        )

    def initialize(
        self,
        goal: str
    ):

        state = RuntimeState(
            goal=goal
        )

        state.status = (
            "running"
        )

        return state

    def observe(
        self,
        state: RuntimeState,
        user_id: str
    ):

        profile = (
            self.profile_manager.load_profile(
                user_id
            )
        )

        if profile:

            state.profile_snapshot = (
                profile.model_dump()
            )

            state.observations.append(

                f"Current Goal: "
                f"{profile.primary_goal}"
            )

            state.observations.append(

                f"Reflection Score: "
                f"{profile.reflection_score}"
            )

            state.observations.append(

                f"Missing Skills: "
                f"{len(profile.missing_skills)}"
            )

        else:

            state.observations.append(
                "No profile found."
            )

        return state

    def plan(
        self,
        state: RuntimeState
    ):

        if not state.plan:

            state.plan = [

                "Research Goal",

                "Identify Skills",

                "Generate Roadmap"
            ]

        return state

    def act(
        self,
        state: RuntimeState
    ):

        if state.plan:

            state.current_task = (
                state.plan.pop(0)
            )

            state.actions_taken.append(

                f"Executed: "
                f"{state.current_task}"
            )

            state.completed_tasks.append(

                state.current_task
            )

        return state

    def reflect(
        self,
        state: RuntimeState
    ):

        state.observations.append(

            f"Completed "
            f"{len(state.completed_tasks)} "
            f"tasks"
        )

        return state

    def finish(
        self,
        state: RuntimeState
    ):

        state.status = (
            "completed"
        )

        return state

    def run(
        self,
        goal: str,
        user_id: str
    ):

        state = self.initialize(
            goal
        )

        state = self.observe(
            state,
            user_id
        )

        state = self.plan(
            state
        )

        while state.plan:

            state.iteration_count += 1

            state = self.act(
                state
            )

            state = self.reflect(
                state
            )

        state = self.finish(
            state
        )

        return state