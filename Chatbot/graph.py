"""
LangGraph graph builder.
"""

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

import config
from nodes import chatbot_node
from state import ChatState


def build_graph():
    builder = StateGraph(ChatState)

    builder.add_node("chatbot", chatbot_node)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)

    conn = sqlite3.connect(config.SQLITE_DB_PATH, check_same_thread=False)
    checkpointer = SqliteSaver(conn=conn)

    return builder.compile(checkpointer=checkpointer)