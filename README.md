# Self-Evaluating Lesson Content Generator

## Project Overview

This project is an AI-powered lesson generation system that creates beginner-friendly educational content and evaluates its quality automatically.

It uses a Generator and an Evaluator workflow. If a generated lesson fails the evaluation, the system sends feedback to the Generator and attempts to improve the lesson.

The project uses LangGraph to manage the workflow and SQLite to store lesson history and evaluation results.

## Key Features

- Generates beginner-friendly educational lessons.
- Evaluates lessons using six quality criteria.
- Detects possible joined-word and spacing errors using Python.
- Automatically retries rejected lessons, with a maximum of three generation attempts.
- Stores lesson history and evaluation results in SQLite.
- Learns from repeated failure patterns and adds improvement suggestions to future prompts.
- Saves the final approved lesson and rejection history.

## Technologies Used

- Python
- Google Gemini API
- LangGraph
- LangChain Google GenAI
- SQLite
- Pytest
- WordNinja

## Project Structure

```text
Rag-Lesson-Generator/
│
├── agents/
│   ├── generator.py
│   ├── evaluator.py
│   └── validator.py
│
├── workflow/
│   └── graph.py
│
├── memory/
│   ├── database.py
│   └── learning.py
│
├── output/
│   ├── final_lesson.md
│   └── rejection_log.json
│
├── prompts/
├── tests/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Rag-Lesson-Generator
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Create a `.env` file in the project root:

```text
GOOGLE_API_KEY=your_google_api_key_here
```

Never commit your actual API key to GitHub.

## Run the Project

```bash
python main.py
```

The workflow generates a lesson, evaluates it, and retries when necessary.

## Run Tests

```bash
python -m pytest tests/ -v
```

## Output Files

- `output/final_lesson.md` — stores the approved lesson.
- `output/rejection_log.json` — stores rejected attempts and evaluator feedback.
- `memory/lesson_memory.db` — stores persistent lesson and evaluation history.

## Self-Evolution

The system identifies repeated evaluation failures from previous runs.

For example, if lessons repeatedly fail the accuracy criterion, the system adds an improvement instruction to future generation prompts.

This improves future outputs through prompt adaptation and persistent memory, without retraining the AI model.

## Project Goal

To build a self-evaluating AI content generation system that improves educational content quality through automated evaluation, feedback, retries, and persistent memory.