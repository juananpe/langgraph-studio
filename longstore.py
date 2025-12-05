from dataclasses import dataclass
from typing import Dict, Any

from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime

@dataclass
class Context:
    user_id: str

class UserInfo(BaseModel):
    """Container for user information."""
    info: Dict[str, Any] = {}
    """REQUIRED: A dictionary with the user data. Example: {"name": "John", "age": 30, "city": "Boston"}"""

@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Save user information to memory.
    
    IMPORTANT: You must wrap all key-value pairs inside the 'info' field.
    
    Correct usage:
        user_info: {"info": {"name": "John", "age": 30, "favorite_color": "blue"}}
    
    Wrong usage (DO NOT do this):
        user_info: {"name": "John", "age": 30}
    """
    # Studio provides the store automatically via runtime.store
    store = runtime.store 
    user_id = runtime.context.user_id 
    store.put(("users",), user_id, user_info.info) 
    return "Successfully saved user info."

agent = create_agent(
    model="gpt-4.1",
    tools=[save_user_info],
    context_schema=Context  # ✅ Keep this
    # store=store  # ❌ Remove this line
)

# Export for LangGraph Studio
__all__ = ["agent"]