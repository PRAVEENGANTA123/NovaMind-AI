"""
=========================================
NovaMind AI - Gemini Service Test
=========================================
"""

import time

from services.ai.gemini_service import GeminiService


def main():

    print("=" * 70)
    print("NovaMind AI - Gemini Service Test")
    print("=" * 70)

    gemini = GeminiService()

    print(f"Model : {gemini.model}")
    print()

    tests = [

        "Hello",

        "What is Artificial Intelligence?",

        "Write a Python function to reverse a string.",

        "Explain Machine Learning in simple words.",

    ]

    for index, prompt in enumerate(tests, start=1):

        print("=" * 70)

        print(f"TEST #{index}")

        print()

        print("PROMPT")
        print(prompt)

        print()

        start = time.perf_counter()

        answer = gemini.generate(prompt)

        elapsed = time.perf_counter() - start

        print("ANSWER")
        print(answer)

        print()

        print(f"Execution Time : {elapsed:.2f} sec")

        print()


if __name__ == "__main__":
    main()