from services.ai.intent_service import IntentService

prompts = [
    "Analyze CSV file",
    "Analyze dataset",
    "Read excel file",
    "Python API",
]

for prompt in prompts:
    result = IntentService.detect(prompt)

    print("=" * 50)
    print("Prompt:", prompt)
    print("Intent:", result.intent)
    print("Confidence:", result.confidence)
    print("Agent:", result.agent)