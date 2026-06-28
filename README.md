# LangChain Agent with Memory and Confirmation

This project demonstrates a LangChain agent that:
- Persists conversation history in a SQLite database.
- Asks for user confirmation before executing any tool.
- Integrates simple tools (calculator and dummy web search).

## Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/langchain-agent.git
cd langchain-agent

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your_api_key_here"
```

## Running the API

```bash
uvicorn app:app --reload
```

The API exposes a single endpoint:

- `POST /chat`
  - Body: `{ "session_id": "unique_session_id", "message": "Your message" }`
  - Response: `{ "response": "Agent's reply" }`

Each session is identified by `session_id`. The agent will store messages in the SQLite database and ask for confirmation before calling any tool.

## Testing

```bash
pytest
```

The tests cover:
- Memory persistence.
- Confirmation wrapper logic.
- End-to-end agent execution with mocked confirmation.

## Project Structure

```
├── agent/
│   ├── __init__.py
│   ├── memory.py
│   ├── tools.py
│   └── confirmation_agent.py
├── app.py
├── tests/
│   ├── test_memory.py
│   ├── test_confirmation.py
│   └── test_agent.py
├── requirements.txt
└── README.md
```

## Extending

- Add new tools by creating a `BaseTool` subclass in `agent/tools.py` and including it in the `tools` list in `confirmation_agent.py`.
- Modify the confirmation logic by providing a custom `confirm_func` when calling `get_agent`.

Enjoy building your own conversational agents!
