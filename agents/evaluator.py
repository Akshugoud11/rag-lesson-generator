
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Create the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0
)


def evaluate_lesson(lesson):

    prompt = f"""
    You are a strict educational content evaluator.

    Evaluate the following beginner lesson about Introduction to RAG.

    LESSON:
    {lesson}

    Check these six criteria:

        1. ACCURACY:
       Are all technical explanations factually correct?

       Check carefully for misleading claims.

       RAG does NOT guarantee 100% accurate answers.
       RAG does NOT completely eliminate hallucinations.
       It can reduce hallucinations by providing relevant
       information, but the retrieved information itself
       may be incorrect or incomplete.

       FAIL the lesson if it claims RAG guarantees accuracy
       or completely prevents hallucinations.

    2. BEGINNER-FRIENDLY LANGUAGE:
       Is the language simple and easy to understand?

    3. PRACTICAL EXAMPLES:
       Does the lesson include clear and useful examples?

    4. JARGON EXPLANATION:
       Are technical terms explained when introduced?

    5. TOPIC COVERAGE:
       Does it explain what RAG is, why it is needed,
       and how retrieval, augmentation, and generation work?

    6. TEACHING FLOW:
   Is the lesson organized in a logical order?

   Carefully inspect every sentence for:
   - Missing spaces between words.
   - Joined words such as "Ifan", "confidentlyguess",
     and "medicalrecords".
   - Spelling mistakes.
   - Grammar mistakes.
   - Broken or confusing sentences.

   Do not ignore small formatting or language errors.

   If you find multiple missing-space errors,
   mark teaching_flow as FAIL.

    STRICT RULES:

    - If any important criterion fails, verdict must be FAIL.
    - Do not approve misleading technical explanations.
    - Do not approve a lesson with serious language problems.
    - Give clear and specific feedback explaining every failure.
    - Approve only when all six criteria pass.

    Return your result in valid JSON only.
    Do not use Markdown code fences.

    Use exactly this JSON structure:

    {{
        "verdict": "PASS or FAIL",
        "criteria": {{
            "accuracy": "PASS or FAIL",
            "beginner_friendly": "PASS or FAIL",
            "examples": "PASS or FAIL",
            "jargon_explanation": "PASS or FAIL",
            "coverage": "PASS or FAIL",
            "teaching_flow": "PASS or FAIL"
        }},
        "feedback": "Explain what is wrong and how to improve it."
    }}
    """

    print("Evaluator is checking the lesson...")

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        content = "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )

    result = json.loads(content)

    return result
