from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from langchain.memory import BaseMemory
from typing import Dict, List

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(String, index=True)
    role = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SQLiteMemoryStore:
    def __init__(self, db_path: str = "sqlite:///memory.db"):
        self.engine = create_engine(db_path, connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_message(self, session_id: str, role: str, content: str):
        session = self.Session()
        msg = Message(session_id=session_id, role=role, content=content)
        session.add(msg)
        session.commit()
        session.close()

    def get_history(self, session_id: str) -> List[Dict]:
        session = self.Session()
        msgs = session.query(Message).filter_by(session_id=session_id).order_by(Message.timestamp).all()
        session.close()
        return [{"role": m.role, "content": m.content} for m in msgs]

class SQLiteLangChainMemory(BaseMemory):
    def __init__(self, store: SQLiteMemoryStore, session_id: str):
        self.store = store
        self.session_id = session_id

    def load_memory_variables(self, inputs: Dict) -> Dict:
        history = self.store.get_history(self.session_id)
        chat_history = [(msg["role"], msg["content"]) for msg in history]
        return {"chat_history": chat_history}

    def save_context(self, inputs: Dict, outputs: Dict):
        self.store.add_message(self.session_id, "user", inputs.get("input", ""))
        self.store.add_message(self.session_id, "assistant", outputs.get("output", ""))

    def clear(self):
        pass
