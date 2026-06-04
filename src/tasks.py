from crewai import Task

def create_tasks(user_request: str, coordinator_agent, writer_agent, researcher_agent) -> list[Task]:
    """Generates the workflow of tasks for the crew to execute based on a user's request.
    
    Args:
        user_request: The custom request provided by the user.
        coordinator_agent: The Task & Schedule Coordinator agent instance.
        writer_agent: The Document & Content Specialist agent instance.
        researcher_agent: The Information & Research Analyst agent instance.
        
    Returns:
        A list of Task objects representing the sequential workflow.
    """
    
    # 1. Research Task (Researcher)
    research_task = Task(
        description=(
            f"Analyze the user's request: '{user_request}'.\n"
            "Perform internet searches to gather the necessary details, facts, latest trends, or context. "
            "Organize these findings into a detailed, coherent markdown research briefing.\n"
            "Save the findings to a file named 'research_briefing.md' using your writing tool."
        ),
        expected_output=(
            "A structured research briefing markdown file containing verified facts, links, "
            "and insights, saved to 'research_briefing.md'."
        ),
        agent=researcher_agent
    )
    
    # 2. Writing Task (Writer)
    writing_task = Task(
        description=(
            f"Read the research findings in 'research_briefing.md' and consider the request: '{user_request}'.\n"
            "Draft the primary documents, letters, reports, summaries, or drafts requested by the user. "
            "Make sure it is written in a clear, executive, and highly professional tone, formatted in Markdown.\n"
            "Save the finalized document to 'executive_output.md' using your writing tool."
        ),
        expected_output=(
            "A high-quality, professional markdown document matching the request, "
            "saved to 'executive_output.md'."
        ),
        agent=writer_agent,
        context=[research_task]  # Pass the context of research task
    )
    
    # 3. Coordination & Review Task (Coordinator)
    coordination_task = Task(
        description=(
            f"Review the drafted work in 'executive_output.md' and the user request: '{user_request}'.\n"
            "Query the current date and time using your tools. "
            "Extract any actionable items, follow-ups, schedule dates, or deadlines from the output. "
            "Formulate a structured action-item roadmap or task checklist with dates, if applicable. "
            "Save this checklist to 'action_plan.md'.\n"
            "Compose a brief, polished final summary report summarizing the completed work, files saved, "
            "and next steps to present to the user."
        ),
        expected_output=(
            "An action plan checklist saved to 'action_plan.md' and a final summary text describing "
            "what was achieved."
        ),
        agent=coordinator_agent,
        context=[research_task, writing_task]
    )
    
    return [research_task, writing_task, coordination_task]
