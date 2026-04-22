"""
Manages chat threads — persistence, listing, creation, deletion.
"""

import json
import os
import sqlite3

import config
from db import delete_messages, load_messages

CHATS_INDEX_PATH = "chats_index.json"


def _load_index() -> dict:
    if not os.path.exists(CHATS_INDEX_PATH):
        return {"active_thread_id": None, "chats": {}}
    with open(CHATS_INDEX_PATH, "r") as f:
        return json.load(f)


def _save_index(index: dict):
    with open(CHATS_INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)


def get_active_thread_id() -> str | None:
    return _load_index().get("active_thread_id")


def set_active_thread_id(thread_id: str):
    index = _load_index()
    index["active_thread_id"] = thread_id
    _save_index(index)


def create_chat(thread_id: str, title: str = "New Chat"):
    index = _load_index()
    index["chats"][thread_id] = {"title": title}
    index["active_thread_id"] = thread_id
    _save_index(index)


def update_chat_title(thread_id: str, title: str):
    index = _load_index()
    if thread_id in index["chats"]:
        index["chats"][thread_id]["title"] = title
        _save_index(index)


def delete_chat(thread_id: str):
    index = _load_index()
    if thread_id in index["chats"]:
        del index["chats"][thread_id]

    if index.get("active_thread_id") == thread_id:
        remaining = list(index["chats"].keys())
        index["active_thread_id"] = remaining[-1] if remaining else None

    _save_index(index)
    delete_messages(thread_id)

    try:
        conn = sqlite3.connect(config.SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM checkpoints WHERE thread_id = ?", (thread_id,))
        cursor.execute("DELETE FROM writes WHERE thread_id = ?", (thread_id,))
        conn.commit()
        conn.close()
    except Exception:
        pass


def list_chats() -> list[dict]:
    index = _load_index()
    return [
        {"thread_id": tid, "title": meta["title"]}
        for tid, meta in index["chats"].items()
    ]


def load_chat_history(thread_id: str) -> list[tuple[str, str]]:
    return load_messages(thread_id)