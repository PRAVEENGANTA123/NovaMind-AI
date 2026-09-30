from services.ai.orchestrator_service import AIOrchestrator


tests = [

    "Write Python API",

    "Summarize Resume.pdf",

    "Compare AWS and Azure",

    "Analyze CSV file",

    "Explain Image",

]


for prompt in tests:

    result = AIOrchestrator.process(prompt)

    print("=" * 70)

    print("PROMPT")
    print(result.prompt)

    print()

    print("INTENT")
    print(result.intent)

    print()

    print("CONFIDENCE")
    print(result.confidence)

    print()

    print("SUCCESS")
    print(result.success)

    print()

    print("TIME")
    print(result.execution_time)

    print()

    print("ANSWER")
    print(result.answer)

    print()