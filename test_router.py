from services.ai.intent_service import IntentService
from services.ai.router_service import RouterService

tests = [

    "Write Python code",

    "Summarize Resume.pdf",

    "Compare AWS and Azure",

    "Analyze CSV",

    "Explain Image",

]

for prompt in tests:

    intent = IntentService.detect(prompt)

    plan = RouterService.create_plan(intent)

    print("=" * 60)

    print(prompt)

    print()

    print("Agent")

    print(plan.agent)

    print()

    print("Tools")

    print(plan.tools)

    print()

    print("Execution")

    for step in plan.steps:

        print("✓", step)