from services.ai.context_service import ContextService


tests = [

    "Write Python API",

    "Summarize Resume.pdf",

    "Compare AWS and Azure",

    "Analyze CSV file",

    "Explain Image",

]


for prompt in tests:

    context = ContextService.build(prompt)

    print("=" * 70)

    print("PROMPT")
    print(context.prompt)

    print()

    print("MEMORY")
    print(context.memory)

    print()

    print("HISTORY")
    print(context.history)

    print()

    print("DOCUMENTS")
    print(context.documents)

    print()

    print("SEARCH RESULTS")
    print(context.search_results)

    print()

    print("USER PREFERENCES")
    print(context.user_preferences)

    print()

    print("METADATA")
    print(context.metadata)

    print()