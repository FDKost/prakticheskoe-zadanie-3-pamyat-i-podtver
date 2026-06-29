import os
from agent import SimpleAgent

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    agent = SimpleAgent(api_key=api_key, auto_confirm=False)
    print("Welcome to the Agent. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        output = agent.process(user_input)
        print(f"Agent: {output}")

if __name__ == "__main__":
    main()
