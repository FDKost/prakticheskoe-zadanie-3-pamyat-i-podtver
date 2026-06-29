import re
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
from memory import PersistentMemory
from confirmation import is_critical_action, confirm_action

class SimpleAgent:
    """
    A lightweight agent that uses LangChain to generate responses,
    stores conversation history persistently, and asks for confirmation
    before executing critical actions.
    """

    def __init__(self, api_key: str, auto_confirm: bool = False):
        self.llm = OpenAI(openai_api_key=api_key, temperature=0.7)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.persistent_memory = PersistentMemory()
        self.auto_confirm = auto_confirm

        self.prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template=(
                "You are an assistant. Use the following conversation history:\n"
                "{history}\n"
                "User: {input}\n"
                "Assistant:"
            ),
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template, memory=self.memory)

    def _get_history(self) -> str:
        messages = self.persistent_memory.get_recent_messages(limit=5)
        return "\n".join([f"{role}: {content}" for role, content in messages])

    def process(self, user_input: str) -> str:
        # Store user input
        self.persistent_memory.add_message("user", user_input)

        # Get context
        history = self._get_history()

        # Run chain
        response = self.chain.run(history=history, input=user_input)

        # Store assistant response
        self.persistent_memory.add_message("assistant", response)

        # Check for critical action in response
        action = self._extract_action(response)
        if action and is_critical_action(action):
            if not confirm_action(action, auto_confirm=self.auto_confirm):
                return f"Action '{action}' cancelled by user."

        # Execute action (placeholder)
        if action:
            return f"Executed action: {action}"
        return response

    def _extract_action(self, text: str) -> str:
        """
        Extract an action keyword from the assistant's response.
        Looks for a line like 'ACTION: <name>'.
        """
        match = re.search(r"ACTION:\s*(\w+)", text, re.IGNORECASE)
        if match:
            return match.group(1).lower()
        return None
