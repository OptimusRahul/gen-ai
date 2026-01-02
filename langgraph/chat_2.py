from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

load_dotenv()

client = OpenAI()

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    print("ChatBot Node", state)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": state["user_query"]}
        ]
    )

    state["llm_output"] = response.choices[0].message.content
    return state

def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    """
    Dynamically evaluate if the response is good enough or needs a second attempt.
    Uses LLM to evaluate the quality of the first response.
    """
    print("evaluate_response Node - state:", state)
    
    # Use LLM to evaluate the response quality
    evaluation_prompt = f"""
    Evaluate if this response properly answers the user's question.
    
    User Question: {state['user_query']}
    AI Response: {state.get('llm_output', '')}
    
    Reply with ONLY 'YES' if the response is complete and accurate, or 'NO' if it needs improvement.
    """
    
    eval_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": evaluation_prompt}
        ]
    )
    
    evaluation = (eval_response.choices[0].message.content or "NO").strip().upper()
    print(f"Evaluation result: {evaluation}")
    
    # If evaluation is positive, go to end, otherwise try with gemini
    if "YES" in evaluation:
        state["is_good"] = True
        return "endnode"
    else:
        state["is_good"] = False
        return "chatbot_gemini"

def chatbot_gemini(state: State):
    """
    Fallback chatbot that tries to generate a better response.
    Uses a more detailed prompt to improve the response.
    """
    print("chatbot_gemini Node", state)
    
    improved_prompt = f"""
    The user asked: {state['user_query']}
    
    Previous response was not satisfactory. Please provide a more detailed, accurate, and helpful response.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": improved_prompt}
        ]
    )

    state["llm_output"] = response.choices[0].message.content
    state["is_good"] = True  # Mark as good after refinement
    return state

def endnode(state: State):
    print("endnode Node", state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke({"user_query": "If a train leaves Chicago at 60mph heading east, and another leaves New York at 80mph heading west, and they're 900 miles apart, when will they meet?"})
print("Updated State", updated_state)