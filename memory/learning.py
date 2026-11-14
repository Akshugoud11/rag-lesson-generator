
import json
from memory.database import get_connection


def save_lesson(topic, lesson, verdict, criteria, feedback):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO lesson_history
        (topic, lesson, verdict, criteria, feedback)
        VALUES (?, ?, ?, ?, ?)
    """, (
        topic,
        lesson,
        verdict,
        json.dumps(criteria),
        feedback
    ))

    connection.commit()
    connection.close()

    print("Lesson history saved successfully!")


def get_lesson_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, topic, verdict, criteria, feedback, created_at
        FROM lesson_history
        ORDER BY id DESC
    """)

    records = cursor.fetchall()
    connection.close()

    return records


def get_improvement_suggestions(topic, min_failures=2):

    records = get_lesson_history()

    failure_counts = {}

    # Check previous failed evaluations
    for record in records:

        record_topic = record[1]
        verdict = record[2]
        criteria = json.loads(record[3])

        if record_topic == topic and verdict == "FAIL":

            for criterion, status in criteria.items():

                if status == "FAIL":
                    failure_counts[criterion] = (
                        failure_counts.get(criterion, 0) + 1
                    )

    # Create improvement instructions
    improvement_rules = {
        "accuracy": "Explain technical facts carefully. Avoid misleading claims.",
        "beginner_friendly": "Use simpler English and explain difficult concepts.",
        "examples": "Include more practical, real-world examples.",
        "jargon_explanation": "Explain every technical term when it first appears.",
        "coverage": "Cover all important parts of the topic.",
        "teaching_flow": "Organize the lesson in a clear logical order."
    }

    suggestions = []

    for criterion, count in failure_counts.items():

        if count >= min_failures:
            suggestions.append(improvement_rules[criterion])

    return suggestions

