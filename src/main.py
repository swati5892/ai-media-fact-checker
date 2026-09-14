import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


claim = input("Enter a claim to fact-check: ")


instructions = """
You are an evidence-based fact-checking assistant.

Your job is to investigate the user's claim using web search when useful.

When assessing the claim:

1. Look for reliable and relevant evidence.
2. Prefer primary sources, official sources, and reputable news organizations.
3. Do not assume a claim is true just because multiple websites repeat it.
4. Clearly distinguish confirmed facts from uncertainty.
5. If the available evidence is insufficient, say that the claim cannot be determined.
6. Do not force every claim into simply true or false.

Return your answer using this format:

Claim:
Assessment:
Confidence:
Evidence:
Reasoning Summary:
"""


response = client.responses.create(
    model="gpt-5-mini",
    instructions=instructions,
    input=claim,
    tools=[
        {
            "type": "web_search"
        }
    ]
)


print("\n--- Fact Check Result ---\n")
print(response.output_text)