from services.ai.tool_router_service import ToolRouterService

tests = [

    "Explain Python",

    "Latest AI News",

    "Summarize https://openai.com",

    "Analyze my PDF",

]

for prompt in tests:

    route = ToolRouterService.detect(prompt)

    print("=" * 60)

    print(prompt)

    print(route)