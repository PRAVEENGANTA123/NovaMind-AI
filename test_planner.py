from services.ai.reasoning_service import ReasoningService
from services.ai.planner_service import PlannerService


tests = [

    "Write Python API",

    "Summarize Resume.pdf",

    "Compare AWS and Azure",

    "Analyze CSV file",

    "Explain Image",

]


for prompt in tests:

    reasoning = ReasoningService.analyze(prompt)

    plan = PlannerService.create(reasoning)

    print("=" * 70)

    print("PROMPT")
    print(prompt)

    print()

    print("TASK")
    print(plan.task)

    print()

    print("AGENT")
    print(plan.agent)

    print()

    print("TOOLS")
    print(plan.tools)

    print()

    print("COMPLEXITY")
    print(plan.complexity)

    print()

    print("ESTIMATED TIME")
    print(plan.estimated_time)

    print()

    print("EXECUTION PLAN")

    for step in plan.steps:
        print("✓", step)

    print()