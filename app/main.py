from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel

from app.agent_graph import build_graph
from langchain_core.messages import HumanMessage

graph = build_graph()

app = FastAPI(title="LangGraph Agent API")


class Query(BaseModel):
    question: str


@app.post("/ask")
def ask(query: Query) -> Dict:
    """Send a question to the agent and return the messages."""
    # Initial state with human message
    initial_state = {"messages": [HumanMessage(content=query.question)]}

    result = graph.invoke(initial_state)

    messages = []
    for msg in result["messages"]:
        messages.append(
            {
                "type": msg.type,
                "content": getattr(msg, "content", ""),
                "tool_calls": getattr(msg, "tool_calls", None),
            }
        )

    return {"messages": messages}
