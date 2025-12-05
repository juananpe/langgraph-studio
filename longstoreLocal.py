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
    store.put(("users",), user_id, data) 
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
    agent = create_agent(
        model="gpt-4.1",
        tools=[save_user_info, get_user_info],
        context_schema=Context,  # ✅ Keep this
        store=store  # ✅ Keep this
    )

    # Test it
    if __name__ == "__main__":
        result = agent.invoke(
            {"messages": [{"role": "user", "content": "My name is John Smith"}]},
            context=Context(user_id="user_123")
        )
        print("✅ Agent result:", result["messages"][-1].content)
        
        # Verify data persisted
        saved = store.get(("users",), "user_123")
        print("💾 Saved data:", saved.value if saved else "No data")