"""
Streamlit UI for the LangGraph chatbot.

Usage:
    streamlit run app.py
"""

import streamlit as st
from graph import build_graph
from utils import generate_thread_id

# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

st.set_page_config(page_title="LangGraph Chatbot", layout="wide")


@st.cache_resource
def _get_graph():
    return build_graph()


graph = _get_graph()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "thread_id" not in st.session_state:
    st.session_state.thread_id = generate_thread_id()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------------------------------------------------------
# UI Header
# ---------------------------------------------------------------------------

st.title("🤖 LangGraph Chatbot")
st.caption(f"Thread ID: `{st.session_state.thread_id}`")

# ---------------------------------------------------------------------------
# Render chat history
# ---------------------------------------------------------------------------

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        final_answer = ""

        run_config = {
            "configurable": {"thread_id": st.session_state.thread_id}
        }

        try:
            for msg_chunk, metadata in graph.stream(
                {"question": user_input, "answer": "", "messages": []},
                config=run_config,
                stream_mode="messages",
            ):
                if metadata.get("langgraph_node") == "chatbot":
                    token = getattr(msg_chunk, "content", "")
                    if token:
                        final_answer += token
                        response_placeholder.markdown(final_answer)

        except Exception as e:
            final_answer = f"Error: {str(e)}"
            response_placeholder.markdown(final_answer)

        st.session_state.chat_history.append(("assistant", final_answer))