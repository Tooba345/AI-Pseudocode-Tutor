from utils.api_client import ClaudeClient


client = ClaudeClient()

response = client.ask(
    "Explain what a variable is to a Cambridge 9618 A Level Computer Science student."
)

print(response)