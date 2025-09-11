# test_graph.py

from app.agent_graph import build_graph  # or replace with the actual file path
from langchain_core.messages import HumanMessage


def main():
    graph = build_graph()

    # user_input = "What is the capital of France?"
    user_input = "What is 6 times 7?"
    initial_state = {"messages": [HumanMessage(content=user_input)]}
    g = graph.get_graph()

    # Print Mermaid diagram code
    print(g.draw_mermaid())
    result = graph.invoke(initial_state)

    print("=== Final Output ===")
    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}")


if __name__ == "__main__":
    main()
