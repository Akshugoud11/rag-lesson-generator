
from types import SimpleNamespace
import agents.generator as generator


def test_generator_uses_improvement_suggestions(monkeypatch):

    captured_prompt = {}

    # Simulate a previous failure improvement suggestion
    def fake_suggestions(topic):
        return [
            "Explain technical facts carefully. Avoid misleading claims."
        ]

    # Replace the Gemini API call with a test function
    def fake_invoke(self, prompt):
        captured_prompt["text"] = prompt
        return SimpleNamespace(content="Test lesson generated")

    monkeypatch.setattr(
        generator,
        "get_improvement_suggestions",
        fake_suggestions
    )

    monkeypatch.setattr(
        type(generator.llm),
        "invoke",
        fake_invoke
    )

    # Generate a test lesson
    result = generator.generate_lesson("Introduction to RAG")

    # Check the result
    assert result == "Test lesson generated"

    # Check whether the improvement instruction was included
    assert "Explain technical facts carefully" in captured_prompt["text"]

    print("Self-evolution workflow test passed!")
