from app.runtime.runtime_models import (
    RuntimeState
)

from app.profile.profile_manager import (
    ProfileManager
)

from app.research.research_agent import (
    ResearchAgent
)

from app.rag.rag_engine import (
    RAGEngine
)


class RuntimeLoop:

    def __init__(self):

        self.profile_manager = (
            ProfileManager()
        )

        self.research_agent = (
            ResearchAgent()
        )

        self.rag_engine = (
            RAGEngine()
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

        if state.plan:

            return state

        profile = (
            state.profile_snapshot
        )

        if not profile:

            state.plan = [

                "Research Goal",

                "Identify Skills",

                "Generate Roadmap"
            ]

            return state

        missing_skills = (

            profile.get(
                "missing_skills",
                []
            )
        )

        projects = (

            profile.get(
                "projects",
                []
            )
        )

        generated_plan = []

        for skill in missing_skills:

            generated_plan.append(
                f"Learn {skill}"
            )

        if len(projects) < 3:

            generated_plan.append(
                "Build Portfolio Project"
            )

        generated_plan.append(
            "Apply For Opportunities"
        )

        state.plan = (
            generated_plan
        )

        return state

    def act(
        self,
        state: RuntimeState
    ):

        if not state.plan:

            return state

        state.current_task = (
            state.plan.pop(0)
        )

        research = (
            self.research_agent.research(
                state.current_task
            )
        )

        rag_result = (
            self.rag_engine.generate(
                state.current_task
            )
        )

        state.action_results[
            state.current_task
        ] = {

            "research": {

                "query": research.query,

                "evidence": research.evidence,

                "conclusion": research.conclusion
            },

            "rag": rag_result[
                "response"
            ]
        }

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