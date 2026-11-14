
import pytest
from memory import database, learning


@pytest.fixture
def temporary_database(tmp_path, monkeypatch):

    # Use a separate temporary database for testing
    test_db = tmp_path / "test_memory.db"

    monkeypatch.setattr(database, "DB_PATH", test_db)

    # Create the database table
    database.create_table()


def test_save_and_retrieve_lesson(temporary_database):

    learning.save_lesson(
        "Introduction to RAG",
        "Test lesson",
        "PASS",
        {"accuracy": "PASS"},
        "No issues"
    )

    history = learning.get_lesson_history()

    assert len(history) == 1
    assert history[0][1] == "Introduction to RAG"
    assert history[0][2] == "PASS"


def test_repeated_failures_generate_suggestions(temporary_database):

    # Save two failed evaluations for the same topic
    for _ in range(2):

        learning.save_lesson(
            "Introduction to RAG",
            "Test lesson",
            "FAIL",
            {"accuracy": "FAIL"},
            "Accuracy needs improvement"
        )

    suggestions = learning.get_improvement_suggestions(
        "Introduction to RAG"
    )

    assert len(suggestions) > 0
    assert any("technical facts carefully" in item for item in suggestions)
