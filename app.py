import os
import sys
import io
import time
import threading
import streamlit as st
from dotenv import load_dotenv

try:
    from streamlit.runtime.scriptrunner_utils.script_run_context import get_script_run_ctx, add_script_run_ctx
except ImportError:
    from streamlit.runtime.scriptrunner import get_script_run_ctx, add_script_run_ctx

# Ensure the local src folder can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the crew logic
from src.crew import run_executive_crew

# Load environment variables
load_dotenv()

# Streamlit Page Config
st.set_page_config(
    page_title="Executive Crew - AI Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .file-item {
        padding: 0.5rem;
        background-color: #E5E7EB;
        border-radius: 5px;
        margin-bottom: 0.5rem;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# Helper: Redirect stdout to capture agent thoughts in real-time safely across multiple threads
class StdoutRedirector:
    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.stream = io.StringIO()
        self.original_stdout = sys.stdout
        # Store context from main thread
        self.context = get_script_run_ctx()

    def write(self, data):
        self.stream.write(data)
        self.original_stdout.write(data)
        
        # Associate main thread context with current worker thread if missing
        if self.context:
            current_thread = threading.current_thread()
            if get_script_run_ctx() is None:
                add_script_run_ctx(current_thread, self.context)
                
        try:
            # Update the Streamlit placeholder with the accumulated log
            self.placeholder.text_area(
                "Agent Thought Process & Execution Logs",
                value=self.stream.getvalue(),
                height=300,
                disabled=True
            )
        except Exception:
            # Silently fallback if context registration fails or UI is closed
            pass

    def flush(self):
        self.original_stdout.flush()

    def __enter__(self):
        sys.stdout = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout


# Initialize API Key in Session State
if "gemini_api_key" not in st.session_state:
    st.session_state["gemini_api_key"] = os.getenv("GEMINI_API_KEY", "")

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">⚙️ Configuration</p>', unsafe_allow_html=True)
    
    # Input for API key
    api_key_input = st.text_input(
        "Gemini API Key",
        value=st.session_state["gemini_api_key"],
        type="password",
        help="Get a key from https://aistudio.google.com/"
    )
    
    if api_key_input:
        st.session_state["gemini_api_key"] = api_key_input
        os.environ["GEMINI_API_KEY"] = api_key_input
        
    st.markdown("---")
    
    st.markdown('<p class="sidebar-title">📁 Workspace Files</p>', unsafe_allow_html=True)
    
    # Function to list current workspace files
    def get_workspace_files():
        ignored = [".venv", "__pycache__", ".git", ".env", ".gitignore", "src"]
        try:
            files = os.listdir(".")
            return [f for f in files if f not in ignored and not f.startswith(".")]
        except Exception:
            return []
            
    workspace_files = get_workspace_files()
    
    if not workspace_files:
        st.info("No generated files in workspace yet.")
    else:
        # Create selector to inspect file
        selected_file = st.selectbox(
            "Select file to view:",
            options=["None"] + sorted(workspace_files)
        )
        
        if selected_file != "None":
            st.markdown(f"**Viewing: `{selected_file}`**")
            try:
                with open(selected_file, "r", encoding="utf-8") as f:
                    content = f.read()
                if selected_file.endswith(".md"):
                    st.markdown(content)
                else:
                    st.code(content)
            except Exception as e:
                st.error(f"Error reading file: {e}")

# --- Main App Layout ---
st.markdown('<p class="main-header">💼 Executive Crew</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Collaborative Multi-Agent Executive Assistant powered by CrewAI & Gemini</p>', unsafe_allow_html=True)

# Instructions card
st.info(
    "💡 **How it works:** Enter a complex task or query. The **Information Analyst** will search the web for facts, "
    "the **Document Specialist** will draft the report/document, and the **Task Coordinator** will organize schedule dates, "
    "verify requirements, and outline an action plan roadmap. All documents will be saved directly into the workspace."
)

# User Request Panel
user_prompt = st.text_area(
    "What would you like the Executive Crew to handle today?",
    placeholder=(
        "e.g., 'Research recent breakthroughs in solid state batteries and write a summary brief for investors. "
        "Include schedule checkpoints for Q3 2026.'"
    ),
    height=120
)

# Launch Button
col1, col2 = st.columns([1, 5])
with col1:
    launch_btn = st.button("🚀 Kickoff Crew", type="primary", use_container_width=True)

if launch_btn:
    if not st.session_state["gemini_api_key"]:
        st.error("🔑 Please set your Gemini API Key in the sidebar configuration first!")
    elif not user_prompt.strip():
        st.warning("📝 Please enter a task request before kicking off the crew.")
    else:
        # Execution feedback containers
        status_box = st.empty()
        log_box = st.empty()
        
        with status_box.container():
            st.markdown("### 🔄 Orchestrating Executive Crew...")
            spinner_ph = st.empty()
            
        with spinner_ph:
            st.spinner("Executing task pipeline...")

        # Setup standard output redirector
        log_placeholder = log_box.empty()
        
        start_time = time.time()
        
        try:
            # Execute crew kickoff capturing stdout logs
            with StdoutRedirector(log_placeholder):
                crew_result = run_executive_crew(user_prompt)
                
            elapsed_time = time.time() - start_time
            status_box.success(f"✅ Execution completed successfully in {elapsed_time:.1f} seconds!")
            
            # Display results
            st.markdown("## 📊 Crew Execution Output")
            
            # Setup Tabs for Files
            tabs = st.tabs(["📝 Final Summary", "🔍 Research Briefing", "📄 Executive Output", "🗓️ Action Plan"])
            
            with tabs[0]:
                st.markdown(crew_result)
                
            with tabs[1]:
                if os.path.exists("research_briefing.md"):
                    with open("research_briefing.md", "r", encoding="utf-8") as f:
                        st.markdown(f.read())
                else:
                    st.warning("Research briefing file was not generated.")
                    
            with tabs[2]:
                if os.path.exists("executive_output.md"):
                    with open("executive_output.md", "r", encoding="utf-8") as f:
                        st.markdown(f.read())
                else:
                    st.warning("Executive output file was not generated.")
                    
            with tabs[3]:
                if os.path.exists("action_plan.md"):
                    with open("action_plan.md", "r", encoding="utf-8") as f:
                        st.markdown(f.read())
                else:
                    st.warning("Action plan file was not generated.")
            
            # Force refresh file selection
            st.rerun()
            
        except Exception as e:
            status_box.empty()
            st.error(f"❌ An error occurred during crew execution:\n{e}")
            st.exception(e)
