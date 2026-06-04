# 💼 Executive Crew - Multi-Agent AI Assistant

**Executive Crew** is a standalone Python multi-agent system powered by **CrewAI** and **Gemini**. It coordinates specialized AI agents (Research Analyst, Writer, and Task Coordinator) to handle research, document creation, and scheduling in a seamless, sequential workflow. It features an interactive **Streamlit** dashboard with a live agent log monitor.

---

## 🛠️ Tech Stack & Architecture

- **Backend**: CrewAI framework, Python 3.12+
- **LLM**: Google Gemini (`gemini-1.5-flash`)
- **Frontend**: Streamlit
- **Tools**: DuckDuckGo Search, Custom File System, Current Date/Time Retriever

---

## 🚀 Getting Started

### 1. Configure the API Key
Create a `.env` file in the root directory (one has been pre-created as a template for you). Update it with your **Gemini API Key**:

```bash
# In .env file
GEMINI_API_KEY=your_gemini_api_key_here
```

*Note: You can also enter the API key directly in the web UI sidebar at runtime!*

### 2. Activate the Virtual Environment
Open your terminal (PowerShell/Command Prompt) and run:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 3. Run the Streamlit Dashboard
Launch the web interface locally:

```bash
streamlit run app.py
```

Streamlit will open the dashboard automatically in your browser at `http://localhost:8501`.

---

## 👥 Meet the Crew

1. **Information & Research Analyst**: Search the internet for facts, verify details, and compile structured research briefings saved directly in the workspace as `research_briefing.md`.
2. **Document & Content Specialist**: Reviews the research briefing and drafts the requested report, memo, template, or email in a professional executive tone, saved in `executive_output.md`.
3. **Task & Schedule Coordinator**: Monitors the current date/time, checks requirements, extracts action items/deadlines from the document, and creates a roadmap saved in `action_plan.md`.
