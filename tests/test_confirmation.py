import unittest
from confirmation import is_critical_action, confirm_action
from unittest.mock import patch

class TestConfirmation(unittest.TestCase):
    def test_is_critical_action(self):
        self.assertTrue(is_critical_action("send_message"))
        self.assertFalse(is_critical_action("greet"))

    @patch('builtins.input', side_effect=['n'])
    def test_confirm_action_decline(self, mock_input):
        result = confirm_action("send_message", auto_confirm=False)
        self.assertFalse(result)

    @patch('builtins.input', side_effect=['y'])
    def test_confirm_action_accept(self, mock_input):
        result = confirm_action("send_message", auto_confirm=False)
        self.assertTrue(result)

    def test_auto_confirm(self):
        self.assertTrue(confirm_action("send_message", auto_confirm=True))

if __name__ == "__main__":
    unittest.main()
