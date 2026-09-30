from services.ai.reasoning_service import ReasoningService
from services.ai.planner_service import PlannerService
from services.ai.execution_service import ExecutionService


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

    result = ExecutionService.execute(plan)

    print("=" * 70)

    print("PROMPT")
    print(prompt)

    print()

    print("SUCCESS")
    print(result.success)

    print()

    print("EXECUTION TIME")
    print(result.execution_time)

    print()

    print("COMPLETED STEPS")

    for step in result.completed_steps:
        print("✓", step)

    print()

    print("OUTPUTS")

    for output in result.outputs:
        print(output)

    print()