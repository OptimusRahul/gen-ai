from dotenv import load_dotenv
import speech_recognition as sr
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio

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


def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 2

        SYSTEM_PROMPT = """
            You're an expert voice agent. You are given the transcript of what
            user has said using voice.
            You need to output as if you are an voice agent and whatever you speak
            will be converted back to audio using AI and played back to user.
        """

        messages = [{"role": "system", "content": SYSTEM_PROMPT},]

        while True:

            print("Speak Something...")
            audio = recognizer.listen(source)

            print("Processing Audio... (STT)")
            stt = recognizer.recognize_google(audio)

            print("You said: ", stt)

            messages.append({"role": "user", "content": stt})

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            print("🤖: ", response.choices[0].message.content)
            asyncio.run(tts(response.choices[0].message.content))

main()