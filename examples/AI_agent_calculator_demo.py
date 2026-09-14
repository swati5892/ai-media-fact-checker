import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def add_numbers(a,b):
	return a+b;

tools = [
    {
        "type": "function",
        "name": "add_numbers",
        "description": "Add two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number."
                },
                "b": {
                    "type": "number",
                    "description": "The second number."
                }
            },
            "required": ["a", "b"],
            "additionalProperties": False
        }
    }
]

response  = client.responses.create(
		model="gpt-5-mini",
		input="what is 120 plus 380",
		tools=tools,
		tool_choice="required"
	)

print(response.output)

for item in response.output:

    if item.type == "function_call" and item.name == "add_numbers":

        arguments = json.loads(item.arguments)

        result = add_numbers(
            arguments["a"],
            arguments["b"]
        )

        print("Tool requested:", item.name)
        print("Arguments:", arguments)
        print("Tool result:", result)

        second_response = client.responses.create(
            model="gpt-5-mini",
            previous_response_id=response.id,
            input=[
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": str(result)
                }
            ],
            tools=tools
        )

        print("Final answer:", second_response.output_text)