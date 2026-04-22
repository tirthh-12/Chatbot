"""
Owns the application data layer.
All reads and writes to chat_messages go through here.
LangGraph checkpointer tables are never touched.
"""

import sqlite3
import config


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(config.SQLITE_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_messages (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id   TEXT    NOT NULL,
                role        TEXT    NOT NULL,
                content     TEXT    NOT NULL,
                created_at  DATETIME DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()


def save_message(thread_id: str, role: str, content: str):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO chat_messages (thread_id, role, content) VALUES (?, ?, ?)",
            (thread_id, role, content),
        )
        conn.commit()


def load_messages(thread_id: str) -> list[tuple[str, str]]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT role, content FROM chat_messages WHERE thread_id = ? ORDER BY id ASC",
            (thread_id,),
        ).fetchall()
    return [(row["role"], row["content"]) for row in rows]


def delete_messages(thread_id: str):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM chat_messages WHERE thread_id = ?",
            (thread_id,),
        )
        conn.commit()