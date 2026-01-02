# Chain of Thought Prompting

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
    You're an expert AI assistant in resolving user queries using chain of thought.
    Your work on START, PLAN and OUTPUT steps.
    You need to PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly follow the given JSON output format.
    - Only run one step at a time.
    - The sequence of steps is START (where usersr gives an input), PLAN (That can be multiple times) and finally OUTPUT 9which is going to be displayed to the user).

    Output JSON Format:
    {"step": "START" | "PLAN" | "OUTPUT", "content": "string"}

    Example:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: {"step": "PLAN": "content": "Seems like user is intrested in math problem"}
    PLAN: {"step": "PLAN": "content": "looking at the problem, we should solve it using BODMAS method"}
    PLAN: {"step": "PLAN": "content": "Yes, The BODMAS is correct method to solve the problem"}
    PLAN: { "step": "PLAN": "content": "first we must multiply 3 * 5 which is 15" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN": "content": "We must perform divide that is 15 / 10  = 1.5" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN": "content": "Now finally lets perform the add 3.5" }
    PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as ans" }
    OUTPUT: { "step": "OUTPUT": "content": "3.5" }

"""

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

user_query = input('👉🏻 ')

message_history.append({"role": "user", "content": user_query})

print("\n\n")

while True:
    response = client.chat.completions.create(  # type: ignore
        model="gpt-4o",
        messages=message_history,
        response_format={"type": "json_object"}
    )
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠", parsed_result.get("content"))
        continue
    
    if parsed_result.get("step") == "OUTPUT":
        print("🤖", parsed_result.get("content"))
        break

# response = client.chat.completions.create(
#     model="gemini-2.5-flash",
#     response_format={"type": "json_object"},
#     messages=[
#         {   "role": "system", # system message is the message that the model will use to guide its behavior
#             "content": SYSTEM_PROMPT
#         },
#         {
#             "role": "user",
#             "content": "Hey, write a code to add 'n' numbers in js?"
#         },
#         {"role": "assistant", "content": json.dumps({"step": "START", "content": "You want a JavaScript code to add 'n' numbers." })},
#         {"role": 'assistant', "content": json.dumps({"step": "PLAN", "content": "I need to write a JavaScript function that can accept any number of arguments and return their sum. I will use the rest parameter `...numbers` to collect all arguments into an array and then use the `reduce` method to calculate the sum."})},
#         {"role": 'assistant', "content": json.dumps({"step": "PLAN", "content": "I will define a JavaScript function called `sumNumbers` that takes a variable number of arguments using the rest parameter `...numbers`. Inside the function, I will use the `reduce` array method to iterate over the `numbers` array and calculate their sum. Finally, I will return the calculated sum and provide an example of how to use the function."})},
#     ]
# )

# print(response.choices[0].message.content)