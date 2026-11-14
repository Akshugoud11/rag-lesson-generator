
from agents.validator import validate_spacing


def test_detects_joined_words():

    lesson = "RAGis useful. findthe answer."

    errors = validate_spacing(lesson)

    assert len(errors) > 0
    assert any("RAGis" in error for error in errors)
    assert any("findthe" in error for error in errors)


def test_accepts_correctly_spaced_words():

    lesson = "RAG uses Python and a vector database."

    errors = validate_spacing(lesson)

    assert errors == []

def test_detects_missing_space_after_comma():

    lesson = "However,answer,you need context."

    errors = validate_spacing(lesson)

    assert any(",answer" in error for error in errors)
    assert any(",you" in error for error in errors)


def test_accepts_correct_comma_spacing():

    lesson = "However, answer, you need context."

    errors = validate_spacing(lesson)

    assert errors == []

