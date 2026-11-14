
from workflow.graph import lesson_graph
import json
import os


# Define the lesson topic
topic = "Introduction to RAG"


# Initial workflow state
initial_state = {
    "topic": topic,
    "feedback": "",
    "attempt": 0,
    "rejection_log": [],
    "final_lesson": ""
}


print("\n========== STARTING LANGGRAPH WORKFLOW ==========")


# Execute the LangGraph workflow
result = lesson_graph.invoke(initial_state)


# Get final results
final_lesson = result.get("final_lesson", "")
rejection_log = result.get("rejection_log", [])


# Create output folder
os.makedirs("output", exist_ok=True)


# Save rejection history
with open("output/rejection_log.json", "w", encoding="utf-8") as file:
    json.dump(rejection_log, file, indent=4)


print("\nRejection log saved successfully!")


# Save approved lesson
if final_lesson:

    with open("output/final_lesson.md", "w", encoding="utf-8") as file:
        file.write(final_lesson)

    print("\nFinal lesson saved successfully!")
    print("\nFinal lesson successfully approved!")

else:

    print("\nMaximum attempts reached. No lesson was approved.")
