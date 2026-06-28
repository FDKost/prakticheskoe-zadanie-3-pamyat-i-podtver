from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.memory import SQLiteMemoryStore, SQLiteLangChainMemory
from agent.confirmation_agent import get_agent

app = FastAPI()

memory_store = SQLiteMemoryStore()

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    memory = SQLiteLangChainMemory(memory_store, req.session_id)
    agent = get_agent(memory, req.session_id)
    try:
        response = agent.run(req.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"response": response}
