#!/usr/bin/env python3
"""
LangGraph Agent with Rich console, MemorySaver checkpoint, tool confirmation,
and interrupt handling.
"""

import re
import uuid
from typing import Dict, Any

from rich.console import Console
from rich.prompt import Prompt

from langgraph.checkpoint.memory import MemorySaver
from langgraph import create_agent
from langgraph.graph import Graph

# Global memory placeholder (will be set in main)
memory = None

# Tool implementation
def calculator_tool(a: float, b: float) -> float:
    """Simple calculator that returns the sum of two numbers."""
    return a + b

# Graph nodes
def process_input(state: Dict[str, Any]) -> Dict[str, Any]:
    thread_id = state["thread_id"]
    user_input = state["user_input"]
    memory.add(thread_id, "user", user_input)

    # Exit command
    if user_input.strip().lower() == "exit":
        return {"output": "Goodbye!"}

    # Detect simple add command
    match = re.search(
        r"(?:Сложи|Add)\s+(-?\d+(\.\d+)?)\s+(?:и|and)\s+(-?\d+(\.\d+)?)",
        user_input,
        re.IGNORECASE,
    )
    if match:
        a = float(match.group(1))
        b = float(match.group(3))
        return {"next": "calculator", "tool_args": (a, b)}

    # Default echo reply
    reply = f"Agent: Я получил сообщение: {user_input}"
    memory.add(thread_id, "assistant", reply)
    return {"output": reply}

def calculator(state: Dict[str, Any]) -> Dict[str, Any]:
    # The tool node automatically receives the arguments via state["tool_args"]
    a, b = state["tool_args"]
    result = calculator_tool(a, b)
    reply = f"Agent: {result}"
    memory.add(state["thread_id"], "assistant", reply)
    return {"output": reply}

def response(state: Dict[str, Any]) -> Dict[str, Any]:
    # This node is not used in this simple graph but kept for completeness
    return {"output": ""}

def build_graph() -> Graph:
    graph = Graph()
    graph.add_node("process_input", process_input)
    graph.add_node("calculator", calculator)
    graph.add_node("response", response)
    graph.add_edge("process_input", "calculator")
    graph.add_edge("process_input", "response")
    graph.add_edge("calculator", "response")
    return graph

def main() -> None:
    console = Console()
    global memory
    memory = MemorySaver()
    agent = create_agent(build_graph, checkpointer=memory, interrupt_before=["calculator"])

    thread_id = str(uuid.uuid4())
    config = {"thread_id": thread_id}

    console.print("[bold green]LangGraph Agent started. Type 'exit' to quit.[/bold green]")

    while True:
        try:
            user_input = console.input("> ")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold red]Interrupted. Exiting.[/bold red]")
            break

        if not user_input.strip():
            continue

        # Stream the agent response
        stream = agent.stream(user_input, config)
        for chunk_type, chunk_data in stream:
            if chunk_type == "__interrupt__":
                # Prompt for confirmation
                confirm = Prompt.ask(
                    "Agent: Вы хотите вызвать инструмент? (Y/N)",
                    choices=["Y", "N"],
                    default="N",
                )
                if confirm.upper() == "Y":
                    # Resume after interrupt
                    resume_stream = agent.stream(None, config)
                    for r_type, r_data in resume_stream:
                        if r_type == "output":
                            console.print(r_data)
                    break
                else:
                    console.print("[yellow]Tool call cancelled. Exiting.[/yellow]")
                    return
            elif chunk_type == "output":
                console.print(chunk_data)

        # Persist memory after each turn
        memory.save()

if __name__ == "__main__":
    main()
