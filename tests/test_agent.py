import pytest
from agent.memory import SQLiteMemoryStore, SQLiteLangChainMemory
from agent.confirmation_agent import get_agent

def test_agent_run(tmp_path):
    db_path = f"sqlite:///{tmp_path}/memory.db"
    store = SQLiteMemoryStore(db_path)
    memory = SQLiteLangChainMemory(store, "sess1")
    agent = get_agent(memory, "sess1", confirm_func=lambda name, inp: True)
    response = agent.run("What is 2+2?")
    assert "4" in response
