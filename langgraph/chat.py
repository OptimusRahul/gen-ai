from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(model="gpt-4o", model_provider="openai")

class State(TypedDict):
    messages: Annotated[list[dict], add_messages]

def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}

def samplenode(state: State):
    print("I'm in samplenode", state)
    print("\n\n")
    return {"messages": ["Hi, This is a message from the sample node"]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

updated_state = graph.invoke({"messages": ["Hi, My name is Rahul Srivastava"]})
print("Updated State", updated_state)
