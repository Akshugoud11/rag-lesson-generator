
from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from agents.generator import generate_lesson
from agents.evaluator import evaluate_lesson
from agents.validator import validate_spacing

from memory.learning import save_lesson


# 1. Define the shared workflow state
class LessonState(TypedDict, total=False):

    topic: str
    lesson: str
    feedback: str
    evaluation: dict
    attempt: int
    rejection_log: list
    final_lesson: str


# 2. Generator node
def generate_node(state: LessonState):

    print("\n========== GENERATING LESSON ==========")

    lesson = generate_lesson(
        state["topic"],
        state.get("feedback")
    )

    return {
        "lesson": lesson,
        "attempt": state.get("attempt", 0) + 1
    }


# 3. Evaluator node
def evaluate_node(state: LessonState):

    print("\n========== EVALUATING LESSON ==========")

    lesson = state["lesson"]

    # Evaluate using Gemini
    evaluation = evaluate_lesson(lesson)

    # Validate spacing using Python
    spacing_errors = validate_spacing(lesson)

    print("\nPython validation errors:", spacing_errors)

    # Reject lesson if spacing errors are found
    if spacing_errors:

        evaluation["verdict"] = "FAIL"
        evaluation["criteria"]["teaching_flow"] = "FAIL"

        evaluation["feedback"] += (
            "\nPython Validator found these spacing errors: "
            + "; ".join(spacing_errors)
        )

    # Save this attempt in SQLite
    save_lesson(
        state["topic"],
        lesson,
        evaluation["verdict"],
        evaluation["criteria"],
        evaluation["feedback"]
    )

    # Prepare the rejection history
    rejection_log = state.get("rejection_log", [])

    if evaluation["verdict"] == "FAIL":

        rejection_log = rejection_log + [{
            "attempt": state["attempt"],
            "criteria": evaluation["criteria"],
            "feedback": evaluation["feedback"]
        }]

        return {
            "evaluation": evaluation,
            "feedback": evaluation["feedback"],
            "rejection_log": rejection_log
        }

    # Lesson passed
    return {
        "evaluation": evaluation,
        "final_lesson": lesson,
        "rejection_log": rejection_log
    }


# 4. Decide whether to retry or finish
def route_after_evaluation(state: LessonState):

    if state["evaluation"]["verdict"] == "PASS":

        print("\nLesson approved!")
        return "done"

    if state["attempt"] < 3:

        print("\nLesson rejected. Retrying...")
        return "retry"

    print("\nMaximum attempts reached.")
    return "done"


# 5. Build the LangGraph workflow
workflow = StateGraph(LessonState)

workflow.add_node("generate", generate_node)
workflow.add_node("evaluate", evaluate_node)

workflow.add_edge(START, "generate")
workflow.add_edge("generate", "evaluate")

workflow.add_conditional_edges(
    "evaluate",
    route_after_evaluation,
    {
        "retry": "generate",
        "done": END
    }
)


# 6. Compile the workflow
lesson_graph = workflow.compile()
