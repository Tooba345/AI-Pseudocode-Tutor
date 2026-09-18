from utils.openai_client import OpenAIClient

client = OpenAIClient()

answer = client.ask(
    "Explain what a FOR loop is in Cambridge International A Level Computer Science 9618."
)

print("\n🤖 AI RESPONSE:\n")
print(answer)