import os
from dotenv import load_dotenv
from crewai import Crew, Process
from src.agents import get_llm, create_coordinator_agent, create_writer_agent, create_researcher_agent
from src.tasks import create_tasks

# Load environment variables (such as GEMINI_API_KEY)
load_dotenv()

def run_executive_crew(user_request: str) -> str:
    """Assembles and kicks off the Executive Crew sequential pipeline.
    
    Args:
        user_request: The specific task/instruction provided by the user.
        
    Returns:
        The final output of the crew's execution.
    """
    # Initialize the Gemini LLM
    llm = get_llm()
    
    # Create agents
    coordinator = create_coordinator_agent(llm)
    writer = create_writer_agent(llm)
    researcher = create_researcher_agent(llm)
    
    # Create the task sequence
    tasks = create_tasks(user_request, coordinator, writer, researcher)
    
    # Build the Crew
    crew = Crew(
        agents=[researcher, writer, coordinator],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    # Kickoff the crew execution
    result = crew.kickoff()
    
    # In CrewAI, kickoff returns a CrewOutput object, we convert it to string
    return str(result)
