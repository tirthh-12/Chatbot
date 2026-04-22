"""
Streamlit UI for the LangGraph chatbot.

Usage:
    streamlit run app.py
"""

import streamlit as st
from graph import build_graph
from utils import generate_thread_id
from db import init_db, save_message
from chat_manager import (
    get_active_thread_id,
    set_active_thread_id,
    create_chat,
    update_chat_title,
    delete_chat,
    list_chats,
    load_chat_history,
)

# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

st.set_page_config(page_title="LangGraph Chatbot", layout="wide")

init_db()


@st.cache_resource
def _get_graph():
    return build_graph()


graph = _get_graph()

# ---------------------------------------------------------------------------
# Bootstrap first chat if nothing exists
# ---------------------------------------------------------------------------

if get_active_thread_id() is None:
    first_thread = generate_thread_id()
    create_chat(first_thread, title="New Chat")

# ---------------------------------------------------------------------------
# Session state init
# ---------------------------------------------------------------------------

if "thread_id" not in st.session_state:
    st.session_state.thread_id = get_active_thread_id()
    st.session_state.chat_history = load_chat_history(st.session_state.thread_id)
    st.session_state.loading = False

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("💬 Chats")

    if st.button("➕ New Chat", use_container_width=True):
        new_thread = generate_thread_id()
        create_chat(new_thread, title="New Chat")
        st.session_state.thread_id = new_thread
        st.session_state.chat_history = []
        st.session_state.loading = False
        st.rerun()

    st.divider()

    chats = list_chats()

    for chat in reversed(chats):
        tid = chat["thread_id"]
        title = chat["title"]
        is_active = tid == st.session_state.thread_id

        col1, col2 = st.columns([5, 1])

        with col1:
            button_label = f"**{title}**" if is_active else title
            if st.button(button_label, key=f"chat_{tid}", use_container_width=True):
                if tid != st.session_state.thread_id:
                    st.session_state.thread_id = tid
                    set_active_thread_id(tid)
                    st.session_state.chat_history = load_chat_history(tid)
                    st.session_state.loading = False
                    st.rerun()

        with col2:
            if st.button("🗑", key=f"del_{tid}"):
                delete_chat(tid)
                remaining = list_chats()
                if remaining:
                    next_tid = remaining[-1]["thread_id"]
                    st.session_state.thread_id = next_tid
                    set_active_thread_id(next_tid)
                    st.session_state.chat_history = load_chat_history(next_tid)
                else:
                    new_thread = generate_thread_id()
                    create_chat(new_thread, title="New Chat")
                    st.session_state.thread_id = new_thread
                    st.session_state.chat_history = []
                st.session_state.loading = False
                st.rerun()

# ---------------------------------------------------------------------------
# Main chat UI
# ---------------------------------------------------------------------------

st.title("🤖 LangGraph Chatbot")

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

user_input = st.chat_input("Type your message...", disabled=st.session_state.loading)

if user_input:
    chats = list_chats()
    current_chat = next(
        (c for c in chats if c["thread_id"] == st.session_state.thread_id), None
    )
    if current_chat and current_chat["title"] == "New Chat":
        update_chat_title(st.session_state.thread_id, user_input[:40])

    save_message(st.session_state.thread_id, "user", user_input)
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.loading = True

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("▌")
        final_answer = ""

        run_config = {
            "configurable": {"thread_id": st.session_state.thread_id}
        }

        try:
            result = graph.invoke(
                {"question": user_input, "answer": ""},
                config=run_config,
            )
            final_answer = result.get("answer", "")
            response_placeholder.markdown(final_answer)

        except Exception as e:
            final_answer = f"Error: {str(e)}"
            response_placeholder.markdown(final_answer)

        if final_answer:
            save_message(st.session_state.thread_id, "assistant", final_answer)
            st.session_state.chat_history.append(("assistant", final_answer))

    st.session_state.loading = False