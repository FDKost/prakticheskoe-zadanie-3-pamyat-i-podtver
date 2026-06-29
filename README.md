# Agent with Persistent Memory and Confirmation

This project demonstrates a simple conversational agent built with LangChain that:
- Stores conversation history persistently using SQLite.
- Retrieves recent context before generating responses.
- Requests user confirmation before executing critical actions (e.g., sending messages, changing settings).

## Features

| Feature | Description |
|---------|-------------|
| **Persistent Memory** | Conversation history is stored in `memory.db` and loaded on each interaction. |
| **Context Retrieval** | The last 5 messages are included in the prompt to the LLM. |
| **Confirmation Workflow** | Critical actions are identified and the user is prompted before execution. |
| **Auto-Confirm** | Set `auto_confirm=True` in `SimpleAgent` to bypass prompts (useful for testing). |

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/agent-memory-confirmation.git
   cd agent-memory-confirmation
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set OpenAI API key**

   ```bash
   export OPENAI_API_KEY="your_api_key_here"   # On Windows use `set`
   ```

5. **Run the agent**

   ```bash
   python main.py
   ```

## Usage

- Type any message to the agent.  
- If the agent generates a response containing `ACTION: <name>`, it will ask for confirmation before proceeding.  
- Type `exit` or `quit` to stop the program.

## Testing

Run unit tests with:

```bash
pytest
```

The tests cover:
- Persistence of messages in SQLite.
- Extraction of actions from responses.
- Confirmation logic (both manual and auto-confirm).

## Project Structure

```
├── agent.py          # Main agent logic
├── confirmation.py   # Confirmation utilities
├── memory.py         # Persistent memory implementation
├── main.py           # CLI entry point
├── README.md
├── requirements.txt
└── tests/
    ├── test_memory.py
    └── test_confirmation.py
```

## Extending the Agent

- Add new critical actions to `critical_actions` set in `confirmation.py`.
- Implement actual execution logic in `SimpleAgent.process` where the placeholder comment indicates.
- Adjust the prompt template to include more context or system messages.

Enjoy building smarter agents!
