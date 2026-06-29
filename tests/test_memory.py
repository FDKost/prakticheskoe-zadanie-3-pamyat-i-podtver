import os
import unittest
from memory import PersistentMemory

class TestPersistentMemory(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_memory.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.mem = PersistentMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_add_and_get(self):
        self.mem.add_message("user", "Hello")
        self.mem.add_message("assistant", "Hi")
        msgs = self.mem.get_recent_messages(limit=2)
        self.assertEqual(msgs, [("user", "Hello"), ("assistant", "Hi")])

if __name__ == "__main__":
    unittest.main()
