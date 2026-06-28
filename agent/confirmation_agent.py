from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import BaseTool
from typing import Callable, Dict
from .tools import CalculatorTool, DummySearchTool

def confirmation_wrapper(tool: BaseTool, confirm_func: Callable[[str, str], bool]) -> BaseTool:
    class ConfirmedTool(BaseTool):
        name = tool.name
        description = tool.description

        def _run(self, input: str) -> str:
            if confirm_func(tool.name, input):
                return tool._run(input)
            else:
                return f"Execution of tool '{tool.name}' cancelled by user."
    return ConfirmedTool()

def get_agent(memory, session_id, confirm_func: Callable[[str, str], bool] = None):
    if confirm_func is None:
        def confirm(tool_name: str, input: str) -> bool:
            print(f"Agent wants to call tool '{tool_name}' with input: {input}")
            resp = input("Do you approve? (yes/no): ").strip().lower()
            return resp in ("yes", "y")
    else:
        confirm = confirm_func

    llm = ChatOpenAI(temperature=0)
    tools = [CalculatorTool(), DummySearchTool()]
    confirmed_tools = [confirmation_wrapper(t, confirm) for t in tools]
    agent = initialize_agent(
        confirmed_tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True,
    )
    return agent
