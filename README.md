# langgraph-studio

This project demonstrates a ReAct agent built with LangGraph, utilizing Tavily for web search and Anthropic's Claude model for generation. It's configured to load API keys from a `.env` file.

## Project Setup

1.  **Clone the repository:**
    (The URL will be available after the repository is created on GitHub)
    ```bash
    # git clone <repository_url_once_created>
    # cd langgraph-studio
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    uv pip install -r pyproject.toml
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory (e.g., by copying `.env.example` if one were provided, or create it manually) and add your API keys:
    ```env
    TAVILY_API_KEY="your_tavily_api_key"
    ANTHROPIC_API_KEY="your_anthropic_api_key"
    # OPENAI_API_KEY="your_openai_api_key" # Include if used by your project
    ```
    **Important:** The provided `.gitignore` ensures the `.env` file itself is not committed to the repository.

## Running the Agent

To run the graph defined in `graph.py` using langgraph studio run:
```bash
langgraph dev
```

## Key Components

-   `graph.py`: Defines the LangGraph agent logic, tools, and model interaction.
-   `.env`: Stores API keys (e.g., for Tavily, Anthropic). Loaded by `python-dotenv`.
-   `langgraph.json`: Lists project dependencies for reproducible setup.
-   `.gitignore`: Specifies intentionally untracked files that Git should ignore.
