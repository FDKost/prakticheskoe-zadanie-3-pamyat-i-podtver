#!/usr/bin/env python3
"""
A minimal LangGraph‑style chat agent that demonstrates:
- Rich console output
- Conversation memory per thread
- Tool invocation with user confirmation
- Recursive resume/cancel logic
"""

import uuid
import re
from typing import Dict, List, Tuple, Any, Optional

from rich.console import Console
from rich.prompt import Prompt

# --------------------------------------------------------------------------- #
# Memory implementation
# --------------------------------------------------------------------------- #
class MemorySaver:
    """
    Simple in‑memory conversation store.
    Stores a list of messages per thread_id.
    """
    def __init__(self) -> None:
        self._storage: Dict[str, List[Tuple[str, str]]] = {}

    def add(self, thread_id: str, role: str, content: str) -> None:
        self._storage.setdefault(thread_id, []).append((role, content))

    def get(self, thread_id: str) -> List[Tuple[str, str]]:
        return self._storage.get(thread_id, [])

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
    """
    def __init__(self, memory: MemorySaver, console: Console) -> None:
        self.memory = memory
        self.console = console

    def ask_and_run(
        self,
        user_input: str,
        config: Dict[str, Any],
        resume: bool = False
    ) -> Dict[str, Any]:
        """
        Process a user message.

        Returns a state dict:
            {'next': None}                     # normal reply
            {'next': ('tools',)}               # tool call pending
            {'next': ('exit',)}                # exit command
        """
        thread_id = config["thread_id"]
        self.memory.add(thread_id, "user", user_input)

        # Exit command
        if user_input.strip().lower() == "exit":
            return {"next": ("exit",)}

        # Detect simple add command: "Сложи X и Y" or "Add X and Y"
        match = re.search(r"(?:Сложи|Add)\s+(-?\d+(\.\d+)?)\s+(?:и|and)\s+(-?\d+(\.\d+)?)", user_input, re.IGNORECASE)
        if match:
            a = float(match.group(1))
            b = float(match.group(3))
            # Store tool call info in state
            return {
                "next": ("tools",),
                "tool": "calculator",
                "args": (a, b),
            }

        # Default echo reply
        reply = f"Agent: Я получил сообщение: {user_input}"
        self.memory.add(thread_id, "assistant", reply)
        self.console.print(reply)
        return {"next": None}

# --------------------------------------------------------------------------- #
# Main chat loop
# --------------------------------------------------------------------------- #
def main() -> None:
    console = Console()
    memory = MemorySaver()
    agent = Agent(memory, console)

    # Generate a unique thread id for this session
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

        state = agent.ask_and_run(user_input, config)

        # Handle tool invocation
        if state.get("next") == ("tools",):
            tool_name = state["tool"]
            a, b = state["args"]
            confirm = Prompt.ask(
                f"Agent: Вы хотите вызвать инструмент '{tool_name}'? (yes/no)",
                choices=["yes", "no"],
                default="no",
            )
            if confirm.lower() in ("yes", "y"):
                # Execute tool
                if tool_name == "calculator":
                    result = calculator_tool(a, b)
                    reply = f"Agent: {result}"
                    memory.add(thread_id, "assistant", reply)
                    console.print(reply)
                    # Recursive resume: continue loop to allow next user input
                    continue
                else:
                    console.print(f"[red]Unknown tool: {tool_name}[/red]")
                    break
            else:
                console.print("[yellow]Tool call cancelled. Exiting.[/yellow]")
                break

        # Handle exit
        if state.get("next") == ("exit",):
            console.print("[bold green]Goodbye![/bold green]")
            break

        # Normal loop continues

if __name__ == "__main__":
    main()
