from graph import build_graph
from utils import generate_thread_id


def stream_chat(graph, thread_id: str | None = None):
    if thread_id is None:
        thread_id = generate_thread_id()

    run_config = {
        "configurable": {"thread_id": thread_id}
    }

    print("=" * 50)
    print("LangGraph CLI Chatbot")
    print(f"Thread: {thread_id}")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ("exit", "quit"):
            break

        if not user_input:
            continue

        print("AI: ", end="", flush=True)

        try:
            for msg_chunk, metadata in graph.stream(
                {"question": user_input, "answer": "", "messages": []},
                config=run_config,
                stream_mode="messages",
            ):
                if metadata.get("langgraph_node") == "chatbot":
                    token = getattr(msg_chunk, "content", "")
                    if token:
                        print(token, end="", flush=True)

        except Exception as e:
            print(f"\nError: {str(e)}")

        print()

    return thread_id


if __name__ == "__main__":
    graph_instance = build_graph()
    stream_chat(graph_instance)