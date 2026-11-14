
import re
import wordninja


# Valid technical words and names
IGNORED_WORDS = {
    "chatgpt",
    "embeddings",
    "embedding",
    "chatbot",
    "chatbots",
    "unworn",
    "rightarrow",
    "supersneakers",
    "llm",
    "llms",
    "rag"
}


def validate_spacing(lesson):

    errors = []

    # 1. Detect common text encoding problems
    encoding_errors = [
        "â€",
        "Ã",
        "�",
        "ï¿½"
    ]

    for pattern in encoding_errors:

        if pattern in lesson:
            errors.append(
                f"Possible text encoding issue: {pattern}"
            )

    # 2. Detect common joined words
    known_joined_words = {
    "amodern": "a modern",
    "insteadof": "instead of",
    "breakdownthe": "break down the",
    "orclaude": "or Claude",
    "sometimesgives": "sometimes gives",
    "ornewly": "or newly",
    "thatit": "that it",
    "youmight": "you might",
    "rightinformation": "right information",
    "anai": "an AI",
    "andai": "and AI",
    "capableof": "capable of"
}
   

    for wrong, correct in known_joined_words.items():

        if re.search(r"\b" + re.escape(wrong) + r"\b", lesson, re.IGNORECASE):

            errors.append(
                f"Possible joined words: {wrong} -> {correct}"
            )

    # 3. Detect missing spaces after punctuation
    punctuation_errors = re.findall(
        r"[,;:!?][A-Za-z]+",
        lesson
    )

    for error in punctuation_errors:

        errors.append(
            f"Missing space after punctuation: {error}"
        )

    # 4. Detect joined words using wordninja
    words = re.findall(r"\b[a-zA-Z]+\b", lesson)

    for word in words:

        if len(word) < 5:
            continue

        if word.lower() in IGNORED_WORDS or word.lower() in known_joined_words:
            continue

        split_words = wordninja.split(word)

        if len(split_words) > 1:

            suggestion = " ".join(split_words)

            message = (
                f"Possible joined words: {word} -> {suggestion}"
            )

            if message not in errors:
                errors.append(message)

    return errors
