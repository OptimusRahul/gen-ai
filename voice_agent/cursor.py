# Chain of Thought Prompting
import asyncio
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from pydantic import BaseModel, Field
from typing import Optional, cast, Any
import requests
import json
import os

load_dotenv()

client = OpenAI()

async_client = AsyncOpenAI()

async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create( # type: ignore
        model="gpt-4o-mini-tts",
        voice="coral",
        input=speech,
        instructions="Always speak in cheerful manner with full of delight and happy",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)


def run_command(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    
    # Add headers and timeout to avoid connection issues
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        # Retry up to 3 times with timeout
        for attempt in range(3):
            try:
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    return f"The weather in {city} is {response.text}"
                return "Something went wrong"
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                if attempt == 2:  # Last attempt
                    return f"Could not fetch weather after 3 attempts. Error: {str(e)}"
                print(f"⚠️ Attempt {attempt + 1} failed, retrying...")
                continue
                
    except Exception as e:
        return f"Error fetching weather: {str(e)}"
    
    return "Something went wrong"

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

# Zero shot promping: Directly giving instructions and few examples to the model.
SYSTEM_PROMPT = """
    You're an expert AI assistant in resolving user queries using chain of thought.
    Your work on START, PLAN and OUTPUT steps.
    You need to PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call a tool if required from the list of available tools.
    For every tool call wait for the OBSERVE step which is the output from the called tool.

    Rules:
    - Strictly follow the given JSON output format.
    - Only run one step at a time.
    - The sequence of steps is START (where usersr gives an input), PLAN (That can be multiple times) and finally OUTPUT 9which is going to be displayed to the user).

    Output JSON Format:
    {"step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string"}

    Available Tools:
    - get_weather(city: str): Takes city name as an input string and returns the weather information for the city.
    - run_command(cmd: str): Takes a system linux command as string and executes the command on user's system and returns the output from that command

    Example 1:
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

    Example 2:
    START: Hey, What is the weather of Jaunpur?
    PLAN: {"step": "PLAN": "content": "Seems like user is intrested in weather of Jaunpur in India"}
    PLAN: {"step": "PLAN": "content": "Lets see if we have any available tool from the list of available tools"}
    PLAN: { "step": "PLAN": "content": "Great, we have get_weather tool available for this query." }
    PLAN: { "step": "PLAN": "content": "I need to call get_weather tool for delhi as input for city" }
    PLAN: { "step": "TOOL": "tool": "get_weather", "input": "delhi" }
    PLAN: { "step": "OBSERVE": "tool": "get_weather", "output": "The temp of delhi is cloudy with 20 C" }
    PLAN: { "step": "PLAN": "content": "Great, I got the weather info about delhi" }
    OUTPUT: { "step": "OUTPUT": "content": "The current weather in delhi is 20 C with some cloudy sky." }
"""

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

class MyOutputFormat(BaseModel):
    step: str = Field(...,description="The ID of the step. Example: START, PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call.")
    input: Optional[str] = Field(None, description="The input params for the tool")

recognizer = sr.Recognizer()
microphone = sr.Microphone()

with microphone as source:
    print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(source)
    recognizer.pause_threshold = 2
    while True:
        print("Speak Something...")
        audio = recognizer.listen(source)

        print("Processing Audio... (STT)")
        stt = recognizer.recognize_google(audio)
        print("You said: ", stt)
        message_history.append({"role": "user", "content": stt})

        while True:
            response = client.chat.completions.parse(
                model="gpt-4o",
                response_format=MyOutputFormat,
                messages=cast(Any, message_history),
            )
            raw_result = response.choices[0].message.content or ""
            message_history.append({"role": "assistant", "content": raw_result})

            parsed_result = response.choices[0].message.parsed
            
            if not parsed_result:
                continue

            if parsed_result.step == "START":
                print("🔥", parsed_result.content)
                continue

            if parsed_result.step == "PLAN":
                print("🧠", parsed_result.content)
                continue

            if parsed_result.step == "TOOL":
                tool_to_call = parsed_result.tool
                tool_input = parsed_result.input
                
                if not tool_to_call or not tool_input:
                    continue
                    
                print(f"🛠️: {tool_to_call} ({tool_input})")

                tool_response = available_tools[tool_to_call](tool_input)
                print(f"🛠️: {tool_to_call} ({tool_input}) = {tool_response}")
                message_history.append({"role": "developer", "content": json.dumps({"step": "OBSERVE", "input": tool_input, "output": tool_response})})
                continue

            if parsed_result.step == "OUTPUT":
                print("🤖", parsed_result.content)
                asyncio.run(tts(parsed_result.content))
                break
