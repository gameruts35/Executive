import os
from crewai import Agent, LLM
from src.tools import (
    get_current_datetime, 
    web_search, 
    list_workspace_files, 
    read_file_content, 
    write_file_content
)

def get_llm():
    """Initializes the Gemini LLM for CrewAI agents."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Fallback check for Google API key if specified
        api_key = os.getenv("GOOGLE_API_KEY")
        
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set. Please set it in your environment variables or in the .env file."
        )
    
    # We use gemini/gemini-1.5-flash for fast and reliable performance
    return LLM(
        model="gemini/gemini-1.5-flash",
        api_key=api_key,
        temperature=0.3
    )

def create_coordinator_agent(llm) -> Agent:
    return Agent(
        role="Task & Schedule Coordinator",
        goal="Manage schedules, organize tasks, coordinate items, and track priorities.",
        backstory=(
            "You are a master of organization and time management. You keep track of deadlines, "
            "prioritize tasks, structure checklists, and ensure scheduling coordinates logically without conflicts. "
            "You always use the datetime tool to orient yourself to the current time."
        ),
        tools=[get_current_datetime, list_workspace_files, read_file_content, write_file_content],
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

def create_writer_agent(llm) -> Agent:
    return Agent(
        role="Document & Content Specialist",
        goal="Draft, write, edit, and format professional documents, emails, briefings, and templates.",
        backstory=(
            "You are a highly articulate writer who excels at creating clear, professional, "
            "and persuasive copy. You format items beautifully in Markdown, match the executive tone "
            "perfectly, and produce finalized materials ready for immediate distribution."
        ),
        tools=[list_workspace_files, read_file_content, write_file_content],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_researcher_agent(llm) -> Agent:
    return Agent(
        role="Information & Research Analyst",
        goal="Search the internet, retrieve details, compile data, and verify facts on specific topics.",
        backstory=(
            "You are a meticulous researcher with excellent analytical skills. You search the internet "
            "to find verified, up-to-date facts, filter out noise, summarize main findings, "
            "and format compiled notes for the writing team."
        ),
        tools=[web_search, list_workspace_files, read_file_content, write_file_content],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
