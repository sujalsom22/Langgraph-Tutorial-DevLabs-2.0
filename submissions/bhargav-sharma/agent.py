import operator
import asyncio
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

class AgentState(TypedDict):
    question: str
    messages: Annotated[list, operator.add]
    attempts: int
    final_answer: str


def worker(state: AgentState) -> dict:
    question = state["question"]
    attempt_num = state["attempts"] + 1
    
    prompt = f"Answer this question clearly and in at least 3 sentences: {question}"
    
    response = llm.invoke(prompt)
    
    return {
        "messages": [response.content],
        "attempts": attempt_num,
        "final_answer": response.content
    }


def checker(state: AgentState) -> dict:
    answer = state["final_answer"]
    sentences = answer.split(".")
    
    if len(sentences) >= 3:
        return {"messages": [f"Answer accepted on attempt {state['attempts']}"]}
    else:
        return {"messages": [f"Answer too short, retrying... (attempt {state['attempts']})"]}


def should_retry(state: AgentState) -> str:
    answer = state["final_answer"]
    sentences = [s for s in answer.split(".") if s.strip()]
    
    if state["attempts"] >= 3:
        return "end"
    
    if len(sentences) >= 3:
        return "end"
    
    return "retry"


def build_graph():
    graph = StateGraph(AgentState)
    
    graph.add_node("worker", worker)
    graph.add_node("checker", checker)
    
    graph.set_entry_point("worker")
    graph.add_edge("worker", "checker")
    
    graph.add_conditional_edges("checker", should_retry, {
        "retry": "worker",
        "end": END
    })
    
    return graph

async def main():
    graph = build_graph()
    
    async with AsyncSqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
        app = graph.compile(checkpointer=checkpointer)
        
        config = {"configurable": {"thread_id": "run-2"}}
        
        initial_state = {
            "question": "Why is the sky blue?",
            "messages": [],
            "attempts": 0,
            "final_answer": ""
        }
        
        result = await app.ainvoke(initial_state, config=config)
        
        print("\nFinal Answer ")
        print(result["final_answer"])
        print(f"\nTook {result['attempts']} attempts")
        print("\nMessage Log")
        for msg in result["messages"]:
            print(msg)

asyncio.run(main())