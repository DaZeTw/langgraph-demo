# app/main.py
from fastapi import FastAPI
from copilotkit import LangGraphAGUIAgent
from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from app.agent_graph import build_graph
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph

graph = build_graph()

app = FastAPI()
add_langgraph_fastapi_endpoint(
    app=app,
    agent=LangGraphAGUIAgent(
        name="sample_agent",  # the name of your agent defined in langgraph.json
        description="Describe your agent here, will be used for multi-agent orchestration",
        graph=graph,  # the graph object from your langgraph import
    ),
    path="/sample_agent",  # the endpoint you'd like to serve your agent on
)


@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}
