"""
Shared utility helpers.
"""
import uuid

def generate_thread_id() -> str:
    """Return a new unique thread identifier."""
    return str(uuid.uuid4())
