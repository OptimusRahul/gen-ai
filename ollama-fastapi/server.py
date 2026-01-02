from ollama import Client

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
client = Client(
    host="http://localhost:11434"
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/contact-us")
def contact_us():
    return {"message": "Contact us at contact@example.com"}

@app.post("/chat")
def chat(request: ChatRequest):
    print(f"Received message: {request.message}")
    response = client.chat(model="gemma2:2b", messages=[
        {"role": "user", "content": request.message}
    ])
    print(f"Response: {response}")
    return {"response": response.message.content}
