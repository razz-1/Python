#!/usr/bin/env python3
"""
Interactive Terminal Quiz App
-----------------------------
A text-based multiple-choice quiz that tracks the user's score
and reports a final percentage at the end.
"""

import random
import sys
import time


# ---------------------------------------------------------------------------
# Question Bank
# ---------------------------------------------------------------------------
# Each question is a dict with:
#   "question": the prompt text
#   "options":   list of 4 answer choices
#   "answer":    the correct choice, as a letter ("A", "B", "C", or "D")
#   "category":  optional grouping label
QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "C",
        "category": "Geography",
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": "B",
        "category": "Science",
    },
    {
        "question": "What does 'CPU' stand for?",
        "options": [
            "Central Process Unit",
            "Computer Personal Unit",
            "Central Processing Unit",
            "Central Processor Utility",
        ],
        "answer": "C",
        "category": "Technology",
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen"],
        "answer": "B",
        "category": "Literature",
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "answer": "C",
        "category": "Science",
    },
    {
        "question": "In Python, which keyword is used to define a function?",
        "options": ["func", "def", "function", "lambda"],
        "answer": "B",
        "category": "Technology",
    },
    {
        "question": "How many continents are there on Earth?",
        "options": ["5", "6", "7", "8"],
        "answer": "C",
        "category": "Geography",
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        "answer": "B",
        "category": "Science",
    },
    {
        "question": "Which data structure uses FIFO (First In, First Out) order?",
        "options": ["Stack", "Queue", "Tree", "Graph"],
        "answer": "B",
        "category": "Technology",
    },
    {
        "question": "What year did World War II end?",
        "options": ["1943", "1945", "1947", "1950"],
        "answer": "B",
        "category": "History",
    },
]

LETTERS = ["A", "B", "C", "D"]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def print_header():
    print("=" * 55)
    print(" " * 15 + "PYTHON TERMINAL QUIZ")
    print("=" * 55)
    print("Answer each question by typing A, B, C, or D.")
    print("Type 'quit' at any time to exit early.\n")


def ask_question(index, total, q):
    """Display a single question and return True/False for correct/incorrect."""
    print(f"Question {index}/{total}  [{q.get('category', 'General')}]")
    print(q["question"])
    for letter, option in zip(LETTERS, q["options"]):
        print(f"  {letter}) {option}")

    while True:
        raw = input("\nYour answer: ").strip().upper()

        if raw == "QUIT":
            print("\nQuiz aborted early. Thanks for playing!")
            sys.exit(0)

        if raw in LETTERS:
            break
        print("Please enter A, B, C, D, or 'quit' to exit.")

    correct = raw == q["answer"]
    if correct:
        print("Correct!\n")
    else:
        correct_option = q["options"][LETTERS.index(q["answer"])]
        print(f"Incorrect. The correct answer was {q['answer']}) {correct_option}\n")

    time.sleep(0.4)  # small pause for readability
    return correct


def run_quiz(questions, shuffle=True):
    """Run through all questions and return (score, total)."""
    quiz_questions = questions.copy()
    if shuffle:
        random.shuffle(quiz_questions)

    score = 0
    total = len(quiz_questions)

    for i, q in enumerate(quiz_questions, start=1):
        if ask_question(i, total, q):
            score += 1

    return score, total


def show_results(score, total):
    percentage = (score / total) * 100 if total else 0
    print("=" * 55)
    print("QUIZ COMPLETE")
    print("=" * 55)
    print(f"Score: {score}/{total}")
    print(f"Percentage: {percentage:.1f}%")

    if percentage == 100:
        remark = "Perfect score! Outstanding!"
    elif percentage >= 80:
        remark = "Great job!"
    elif percentage >= 60:
        remark = "Good effort!"
    elif percentage >= 40:
        remark = "Not bad, keep practicing!"
    else:
        remark = "Keep studying and try again!"

    print(remark)
    print("=" * 55)


def main():
    print_header()
    try:
        score, total = run_quiz(QUESTIONS)
        show_results(score, total)
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()