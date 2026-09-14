import base64
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


image_path = input("Enter the path to an image: ")


with open(image_path, "rb") as image_file:
    image_bytes = image_file.read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")


response = client.responses.create(
    model="gpt-5-mini",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": """
Describe only what can be directly observed in this image.

Include:
- main objects or people
- visible environment or setting
- visible text or signs
- notable visual details

Do not guess the exact location, date, event, or backstory unless it is clearly visible in the image.
"""
                },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{encoded_image}"
                }
            ]
        }
    ]
)


print("\n--- Image Analysis ---\n")
print(response.output_text)