from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {   "role": "system", # system message is the message that the model will use to guide its behavior
            "content": "You are an expert in Maths and only and only ans maths realted questions. That if the query is not related to maths. Just say sorry and do not ans that."
        },
        {
            "role": "user",
            "content": "What is the square root of 16?"
        }
    ]
)

print(response.choices[0].message.content)