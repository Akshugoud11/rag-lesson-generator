
from workflow import graph


def test_langgraph_retries_until_lesson_passes(monkeypatch):

    # Count how many times the generator runs
    generation_count = {"count": 0}

    # Simulate lesson generation
    def fake_generate(topic, feedback=None):

        generation_count["count"] += 1

        return f"Test lesson attempt {generation_count['count']}"

    # Simulate evaluator results:
    # First attempt: FAIL
    # Second attempt: FAIL
    # Third attempt: PASS
    evaluation_results = [
        "FAIL",
        "FAIL",
        "PASS"
    ]

    def fake_evaluate(lesson):

        verdict = evaluation_results[generation_count["count"] - 1]

        return {
            "verdict": verdict,
            "criteria": {
                "accuracy": verdict,
                "beginner_friendly": "PASS",
                "examples": "PASS",
                "jargon_explanation": "PASS",
                "coverage": "PASS",
                "teaching_flow": "PASS"
            },
            "feedback": "Improve the lesson"
        }

    # Replace real functions with test functions
    monkeypatch.setattr(graph, "generate_lesson", fake_generate)
    monkeypatch.setattr(graph, "evaluate_lesson", fake_evaluate)

    # Disable actual SQLite writes during this test
    monkeypatch.setattr(graph, "save_lesson", lambda *args: None)

    # Execute LangGraph
    result = graph.lesson_graph.invoke({
        "topic": "Introduction to RAG",
        "attempt": 0,
        "feedback": "",
        "rejection_log": []
    })

    # Verify three attempts occurred
    assert generation_count["count"] == 3

    # Verify the final lesson passed
    assert result["evaluation"]["verdict"] == "PASS"

    # Verify rejected attempts were recorded
    assert len(result["rejection_log"]) == 2

    print("LangGraph retry test passed!")


def test_langgraph_stops_after_three_failures(monkeypatch):

    generation_count = {"count": 0}

    def fake_generate(topic, feedback=None):

        generation_count["count"] += 1
        return "Rejected test lesson"

    def fake_evaluate(lesson):

        return {
            "verdict": "FAIL",
            "criteria": {
                "accuracy": "FAIL",
                "beginner_friendly": "PASS",
                "examples": "PASS",
                "jargon_explanation": "PASS",
                "coverage": "PASS",
                "teaching_flow": "PASS"
            },
            "feedback": "Accuracy needs improvement"
        }

    monkeypatch.setattr(graph, "generate_lesson", fake_generate)
    monkeypatch.setattr(graph, "evaluate_lesson", fake_evaluate)
    monkeypatch.setattr(graph, "save_lesson", lambda *args: None)

    result = graph.lesson_graph.invoke({
        "topic": "Introduction to RAG",
        "attempt": 0,
        "feedback": "",
        "rejection_log": []
    })

    assert generation_count["count"] == 3
    assert len(result["rejection_log"]) == 3
    assert result["evaluation"]["verdict"] == "FAIL"
    assert result.get("final_lesson", "") == ""

