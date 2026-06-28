import pytest
from agent.memory import SQLiteMemoryStore

def test_memory_persistence(tmp_path):
    db_path = f"sqlite:///{tmp_path}/memory.db"
    store = SQLiteMemoryStore(db_path)
    store.add_message("sess1", "user", "Hello")
    store.add_message("sess1", "assistant", "Hi")
    history = store.get_history("sess1")
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
