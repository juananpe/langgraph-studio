from dataclasses import dataclass
import json

from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.store.postgres import PostgresStore
import os

from dotenv import load_dotenv
load_dotenv()

@dataclass
class Context:
    user_id: str

class UserInfo(BaseModel):
    """Container for user information."""
    info: str
    """A JSON string with user data. Example: '{"name": "John", "age": 30, "city": "Boston"}'"""

@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Save user information to memory.
    
    Pass user data as a JSON string in the 'info' field.
    
    Example:
        user_info: {"info": '{"name": "John", "age": 30, "favorite_color": "blue"}'}
    """
    # Studio provides the store automatically via runtime.store
    store = runtime.store 
    user_id = runtime.context.user_id
    # Parse the JSON string to dict before storing
    try:
        data = json.loads(user_info.info)
    except json.JSONDecodeError:
        return "Error: Invalid JSON format. Please provide valid JSON."
    
    # Merge with existing data instead of overwriting
    existing = store.get(("users",), user_id)
    if existing and existing.value:
        merged = {**existing.value, **data}
    else:
        merged = data
    
    store.put(("users",), user_id, merged) 
    return "Successfully saved user info."

@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Look up stored user information.
    
    Use this tool to retrieve any previously saved information about the user,
    such as their name, age, favorite color, pets, occupation, etc.
    """
    store = runtime.store
    user_id = runtime.context.user_id
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "No user information stored yet."

# Use as context manager - tables created automatically on first use
with PostgresStore.from_conn_string(os.getenv("DATABASE_URL")) as store:
    
    store.setup()

    agent = create_agent(
        model="gpt-4.1",
        tools=[save_user_info, get_user_info],
        context_schema=Context,  # ✅ Keep this
        store=store  # ✅ Keep this
    )

    # Conversation loop
    if __name__ == "__main__":
        messages = []
        print("Start chatting with the agent. Type 'quit' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "quit":
                break
            messages.append({"role": "user", "content": user_input})
            result = agent.invoke(
                {"messages": messages},
                context=Context(user_id="EHU")
            )
            messages = result["messages"]
            print("Agent:", result["messages"][-1].content)