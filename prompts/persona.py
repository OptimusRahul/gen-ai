# Persona Based Prompting


from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    # api_key=os.getenv("GEMINI_API_KEY"),
    # base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Zero shot promping: Directly giving instructions and few examples to the model.
SYSTEM_PROMPT = """
    You are an AI Persona Assistant named Rahul Srivastava.
    You are acting on behalf of Rahul Srivastava who is 28 years old Tech enthusiastic and 
    principle engineer. Your main tech stack is JS and Python and You are leaning GenAI these days.

    Examples:
    Q. Hey
    A: Hey, Whats up!

    (100 - 150 examples)
"""


response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT}, 
        {"role": "user", "content": "Hey There"}]
)

print("Response: ", response.choices[0].message.content)
