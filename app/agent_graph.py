from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import BaseMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("Missing OPENAI_API_KEY in environment!")


class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def basic_tool(messages: list[BaseMessage]) -> dict:
    """A basic tool that processes the final answer."""
    last_message = messages[-1].content
    result = f"I have finished processing your question: {last_message}"

    return {"messages": [AIMessage(content=result)]}


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers together."""
    result = a * b
    return result


def route_tools(state: State) -> str:
    """
    Route to 'tools' if the last message includes tool calls, else END.
    """
    messages = state.get("messages", [])
    if not messages:
        raise ValueError("No messages found in state")

    last_msg = messages[-1]

    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"

    return END


def build_graph():
    llm = init_chat_model("openai:gpt-4o-mini", temperature=0)
    tools = [multiply]
    llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

    def chatbot(state: State) -> dict:
        messages = [
            SystemMessage(
                content="You can use the `multiply` tool to help you answer math questions."
            )
        ] + state["messages"]
        response = llm_with_tools.invoke(messages)

        return {"messages": [response]}

    graph = StateGraph(State)

    graph.add_node("chatbot", chatbot)
    graph.add_node("tools", ToolNode(tools=tools))
    graph.add_node("basic_tool", basic_tool)

    graph.add_edge(START, "chatbot")
    graph.add_conditional_edges(
        "chatbot",
        route_tools,
        path_map={
            "tools": "tools",
            END: "basic_tool",
        },
    )

    graph.add_edge("tools", "chatbot")
    graph.add_edge("basic_tool", END)

    return graph.compile()
