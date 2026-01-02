# Zero Shot Prompting

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Zero Shot Prompting is a technique where we don't provide any examples to the model. We just provide the system prompt and the user prompt.
# Zero shot promping: Directly giving instructions to the model.
SYSTEM_PROMPT = "You should only and only ans the coding related questions. Do not ans anything else. Your name is Alexa. If user asks something other than coding, just say sorry."

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {   "role": "system", # system message is the message that the model will use to guide its behavior
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Hey, can you write a python code to print hello world?"
        }
    ]
)

print(response.choices[0].message.content)