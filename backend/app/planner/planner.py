from app.state.state import AgentState


class Planner:

    def create_plan(
        self,
        state: AgentState
    ) -> AgentState:

        goal = state.user_goal.lower()

        if "internship" in goal:

            state.current_plan = [
                "Assess Current Skills",
                "Identify Missing Skills",
                "Build Portfolio Projects",
                "Prepare Resume",
                "Apply To Internships"
            ]

        else:

            state.current_plan = [
                "Analyze Goal",
                "Create Learning Roadmap",
                "Track Progress"
            ]

        return state