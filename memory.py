import sqlite3
from typing import List, Tuple

class PersistentMemory:
    """
    A simple persistent memory store backed by SQLite.
    Stores messages with role (user/assistant) and content.
    """

    def __init__(self, db_path: str = "memory.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def add_message(self, role: str, content: str):
        self.conn.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)", (role, content)
        )
        self.conn.commit()

    def get_recent_messages(self, limit: int = 5) -> List[Tuple[str, str]]:
        cursor = self.conn.execute(
            "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)
        )
        rows = cursor.fetchall()
        return list(reversed(rows))
