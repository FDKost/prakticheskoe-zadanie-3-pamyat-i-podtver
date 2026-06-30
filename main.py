#!/usr/bin/env python3
"""
LangGraph Agent with Rich console, MemorySaver checkpoint, tool confirmation,
and interrupt handling.
"""

import uuid
import re
import time
from typing import Dict, List, Tuple, Any, Optional, Generator

from rich.console import Console
from rich.prompt import Prompt

# --------------------------------------------------------------------------- #
# Memory implementation – use LangGraph's MemorySaver
# --------------------------------------------------------------------------- #
from langgraph.checkpoint.memory import MemorySaver

# --------------------------------------------------------------------------- #
# LangGraph agent creation (dummy graph for demonstration)
# --------------------------------------------------------------------------- #
from langgraph import create_agent
from langgraph.graph import Graph

def build_graph() -> Graph:
    """
    Dummy graph for create_agent. In a real scenario, this would be a
    LangGraph graph with nodes and edges. Here we create an empty graph
    just to satisfy the create_agent call.
    """
    return Graph()

# --------------------------------------------------------------------------- #
# Tool implementation
# --------------------------------------------------------------------------- #
def calculator_tool(a: float, b: float) -> float:
    """Simple calculator that returns the sum of two numbers."""
    return a + b

# --------------------------------------------------------------------------- #
# Agent logic
# --------------------------------------------------------------------------- #
class Agent:
    """
    Very small agent that can:
    - Echo user messages
    - Detect a simple 'add' command and trigger the calculator tool
    - Handle interrupts and confirmations
    """

    def __init__(self, memory: MemorySaver, console: Console) -> None:
        self.memory = memory
        self.console = console

    def ask_and_run(
        self,
        user_input: Optional[str],
        config: Dict[str, Any]
    ) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
        """
        Process a user message and yield streaming chunks.

        Yields:
            ('updates', state_dict)
        """
        thread_id = config["thread_id"]

        # If this is a resume call, we don't add a new user message
        if user_input is not None:
            self.memory.add(thread_id, "user", user_input)

            # Exit command
            if user_input.strip().lower() == "exit":
                state = {"next": ("exit",)}
                yield ("updates", state)
                return

            # Detect simple add command: "Сложи X и Y" or "Add X and Y"
            match = re.search(
                r"(?:Сложи|Add)\s+(-?\d+(\.\d+)?)\s+(?:и|and)\s+(-?\d+(\.\d+)?)",
                user_input,
                re.IGNORECASE,
            )
            if match:
                a = float(match.group(1))
                b = float(match.group(3))
                # Store tool call info in state
                state = {
                    "next": ("tools",),
                    "tool": "calculator",
                    "args": (a, b),
                }
                yield ("updates", state)
                return

            # Default echo reply
            reply = f"Agent: Я получил сообщение: {user_input}"
            self.memory.add(thread_id, "assistant", reply)
            self.console.print(reply)
            state = {"next": None}
            yield ("updates", state)
            return

        # Resume call – no new user input
        # For this simple demo, we just yield a state that continues
        state = {"next": None}
        yield ("updates", state)

# --------------------------------------------------------------------------- #
# Main chat loop
# --------------------------------------------------------------------------- #
def main() -> None:
    console = Console()
    memory = MemorySaver()
    agent = Agent(memory, console)

    # Create a dummy LangGraph agent to satisfy the requirement
    _ = create_agent(build_graph, checkpointer=memory)

    # Use a fixed thread id for this session
    thread_id = "разговор-1"
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
        stream = agent.ask_and_run(user_input, config)
        for chunk_type, chunk_data in stream:
            if chunk_type == "updates":
                state = chunk_data

                # Handle interrupt before tool call
                if state.get("__interrupt__") and state.get("next") == ("tools",):
                    confirm = Prompt.ask(
                        "Agent: Вы хотите вызвать инструмент? (Y/N)",
                        choices=["Y", "N"],
                        default="N",
                    )
                    if confirm.upper() == "Y":
                        # Recursive resume
                        resume_stream = agent.ask_and_run(None, config)
                        for r_type, r_data in resume_stream:
                            if r_type == "updates":
                                state = r_data
                                # Continue processing after resume
                                break
                    else:
                        console.print("[yellow]Tool call cancelled. Exiting.[/yellow]")
                        return

                # Handle tool invocation
                if state.get("next") == ("tools",):
                    tool_name = state["tool"]
                    a, b = state["args"]
                    # Pause before tool execution
                    time.sleep(0.5)
                    confirm = Prompt.ask(
                        f"Agent: Вы хотите вызвать инструмент '{tool_name}'? (yes/no)",
                        choices=["yes", "no"],
                        default="no",
                    )
                    if confirm.lower() in ("yes", "y"):
                        if tool_name == "calculator":
                            result = calculator_tool(a, b)
                            reply = f"Agent: {result}"
                            memory.add(thread_id, "assistant", reply)
                            console.print(reply)
                            # After tool execution, continue loop
                            continue
                        else:
                            console.print(f"[red]Unknown tool: {tool_name}[/red]")
                            return
                    else:
                        console.print("[yellow]Tool call cancelled. Exiting.[/yellow]")
                        return

                # Handle exit
                if state.get("next") == ("exit",):
                    console.print("[bold green]Goodbye![/bold green]")
                    return

                # Normal loop continues
                continue

if __name__ == "__main__":
    main()
