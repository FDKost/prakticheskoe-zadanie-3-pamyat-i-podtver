from langchain.tools import BaseTool
from typing import Dict

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Use this tool to perform arithmetic calculations. Input should be a valid arithmetic expression."

    def _run(self, expression: str) -> str:
        try:
            result = eval(expression, {"__builtins__": {}})
            return str(result)
        except Exception as e:
            return f"Error evaluating expression: {e}"

class DummySearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for a query. Returns a dummy result."

    def _run(self, query: str) -> str:
        return f"Dummy search result for '{query}'."
