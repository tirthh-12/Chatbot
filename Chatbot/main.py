from graph import build_graph
from utils import generate_thread_id


def sanitize_messages(messages):
    """Remove duplicate messages from the list."""
    seen = set()
    sanitized = []
    for message in messages:
        if message.content not in seen:
            sanitized.append(message)
            seen.add(message.content)
    return sanitized


def stream_chat(graph, thread_id: str | None = None):
    if thread_id is None:
        thread_id = generate_thread_id()

    run_config = {"configurable": {"thread_id": thread_id}}

    print("=" * 50)
    print("LangGraph CLI Chatbot")
    print(f"Thread: {thread_id}")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            break

        print("AI: ", end="", flush=True)

        try:
            sanitized_messages = sanitize_messages([])  # Pass sanitized messages
            for chunk, metadata in graph.stream(
                {"question": user_input, "answer": "", "messages": sanitized_messages},
                config=run_config,
                stream_mode="messages",
            ):
                if metadata.get("langgraph_node") != "chatbot":
                    continue
                token = getattr(chunk, "content", "")
                if token:
                    print(token, end="", flush=True)

        except Exception as e:
            print(f"\nError: {e}")

        print()


if __name__ == "__main__":
    stream_chat(build_graph())