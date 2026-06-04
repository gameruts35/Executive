import os
import datetime
from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Get Current Date and Time")
def get_current_datetime() -> str:
    """Returns the current date and time in format YYYY-MM-DD HH:MM:SS. 
    Always run this if you need to know today's date or plan scheduling tasks."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool("Search Internet")
def web_search(query: str) -> str:
    """Searches the internet for a given query and returns search results. 
    Use this to get up-to-date facts, news, or general information."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if not results:
                return f"No search results found for: '{query}'"
            formatted = []
            for r in results:
                formatted.append(f"Title: {r.get('title')}\nLink: {r.get('href')}\nSnippet: {r.get('body')}\n")
            return "\n---\n".join(formatted)
    except Exception as e:
        return f"Error performing web search: {str(e)}"

@tool("List Workspace Files")
def list_workspace_files() -> str:
    """Lists files and folders in the workspace, excluding virtual envs and configuration files. 
    Use this to see what documents are available in the project."""
    try:
        # We assume workspace is the current working directory of the process
        files = os.listdir(".")
        ignored = [".venv", "__pycache__", ".git", ".env", ".gitignore", "src"]
        files = [f for f in files if f not in ignored and not f.startswith(".")]
        if not files:
            return "Workspace is empty (no files found)."
        
        details = []
        for f in files:
            if os.path.isdir(f):
                details.append(f"[Directory] {f}")
            else:
                size = os.path.getsize(f)
                details.append(f"[File] {f} ({size} bytes)")
        return "\n".join(details)
    except Exception as e:
        return f"Error listing workspace files: {str(e)}"

@tool("Read File Content")
def read_file_content(filename: str) -> str:
    """Reads and returns the text content of a file in the workspace. 
    Always verify file existence with List Workspace Files before reading."""
    base = os.path.basename(filename)
    if not os.path.exists(base):
        return f"Error: File '{base}' does not exist in the workspace."
    try:
        with open(base, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{base}': {str(e)}"

@tool("Write File Content")
def write_file_content(filename: str, content: str) -> str:
    """Writes the given text content to a file in the workspace. 
    Creates the file if it doesn't exist, or overwrites it if it does.
    Use this to save briefings, reports, lists, or notes."""
    base = os.path.basename(filename)
    try:
        with open(base, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Success: Content written to '{base}'."
    except Exception as e:
        return f"Error writing file '{base}': {str(e)}"
