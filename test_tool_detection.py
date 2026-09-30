from services.ai.tool_detection_service import ToolDetectionService

tests = [

    "Explain Python inheritance",

    "Latest AI News",

    "Summarize https://openai.com",

    "Analyze my PDF",

]

for prompt in tests:

    print("=" * 60)

    print(prompt)

    print("URL :", ToolDetectionService.has_url(prompt))

    print("WEB :", ToolDetectionService.needs_web_search(prompt))

    print("PDF :", ToolDetectionService.has_pdf(prompt))