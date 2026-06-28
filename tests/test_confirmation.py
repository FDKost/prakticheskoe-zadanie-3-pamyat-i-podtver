import pytest
from agent.confirmation_agent import confirmation_wrapper
from agent.tools import CalculatorTool

def mock_confirm(tool_name, input):
    return True

def test_confirmation_wrapper():
    tool = CalculatorTool()
    wrapped = confirmation_wrapper(tool, mock_confirm)
    result = wrapped.run("1+1")
    assert result == "2"
