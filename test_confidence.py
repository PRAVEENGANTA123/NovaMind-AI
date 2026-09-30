from services.ai.reasoning_service import ReasoningService


tests = [
    "Write Python API",
    "Summarize Resume.pdf",
    "Compare AWS and Azure",
    "Analyze CSV file",
    "Explain Image",
    "Build Flask Login Authentication System",
    "Compare my Resume.pdf with this Job Description",
    "help",
    "fix it",
]


for prompt in tests:

    result = ReasoningService.analyze(prompt)

    print("=" * 70)

    print("PROMPT")
    print(result.prompt)

    print()

    print("INTENT")
    print(result.intent)

    print()

    print("AGENT")
    print(result.agent)

    print()

    print("TOOLS")
    print(result.tools)

    print()

    print("CONFIDENCE")
    print(result.confidence)

    print()

    print("EXECUTION")

    for step in result.execution_plan:
        print("✓", step)

    print()