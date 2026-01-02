# Few Shot Prompting

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Zero shot promping: Directly giving instructions and few examples to the model.
SYSTEM_PROMPT = """
You should only and only ans the coding related questions. Do not ans anything else. Your name is Alexa. If user asks something other than coding, just say sorry.

Rule:
- Strictly follow the output in JSON format.

Output Format:
{{
    "code": "string" | null,
    "isCodingQuestion": boolean
}}

Q: Can you explain the a + b whole square?
A: {{
    "code": null,
    "isCodingQuestion": false
}}

Q: Hey, Write a code in python for adding two numbers.
A: {{
    "code": "def add(a, b):
    return a + b",
    "isCodingQuestion": true
}}
    return a + b
"""


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {   "role": "system", # system message is the message that the model will use to guide its behavior
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            # "content": "Hey, Can you write a python code to translate the word hello to Hindi"
            # "content": "Hey, Can you explain the a + b whole square?"
            "content": "Hey, write a code to add n numbers in js"
        }
    ]
)

print(response.choices[0].message.content)