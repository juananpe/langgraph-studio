from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model

from langchain_tavily import TavilySearch
from langchain_core.tools import tool
import asyncio
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

# Define our TavilySearch tool
tavily_search_tool = TavilySearch(
    max_results=5,
    search_depth="basic"
)

# Wrap the TavilySearch tool in a tool decorator and make it async
@tool
async def search(query: str) -> str:
    """Search for general web results."""
    return await asyncio.to_thread(tavily_search_tool.invoke, {"query": query})

# Store our tools in a list
tools = [search]

# Get today's date for system prompt
today = datetime.now().strftime("%Y-%m-%d")

# Create our system prompt
system_prompt = f"""
You are a helpful assistant that can search the web for information using the search tool.

today's date is {today}
"""

# Define our model
model = init_chat_model(model_provider="anthropic", model="claude-3-7-sonnet-latest")

# Create a ReactAgent with the tools
graph = create_react_agent(model=model, tools=tools, prompt=system_prompt)
